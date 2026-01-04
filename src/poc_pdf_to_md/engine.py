"""Conversion engine coordinating PDF parsing, image extraction, and conversion."""

import hashlib
import json
import os
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Iterable

from .pdf_parser import (
    open_pdf,
    parse_pdf,
    extract_image,
    render_page_as_image,
)
from .image_handler import (
    generate_image_filename,
    generate_page_image_filename,
    save_image,
)
from .parse_result import (
    create_parse_result,
    save_parse_result,
    load_parse_result,
    validate_schema_version,
    validate_block_index_order,
)
from .gemini_client import generate_page_markdown

_PROGRESS_UPDATE_INTERVAL_SEC = 0.1


def _format_duration(seconds: float) -> str:
    """Format seconds as a short, human-readable duration."""
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    return f"{seconds:.1f}s"


class _ProgressPrinter:
    """Print single-line progress updates to a stream (in-place when TTY)."""

    def __init__(self, stream) -> None:
        self._stream = stream
        self._is_tty = bool(getattr(stream, "isatty", lambda: False)())
        self._last_line_len = 0
        self._lock = threading.Lock()

    def update(self, line: str) -> None:
        """Update the current line (TTY) or noop (non-TTY)."""
        if not self._is_tty:
            return

        with self._lock:
            # Clear the whole line first to avoid RPROMPT/right-side artifacts (e.g. stray ')').
            # ANSI: \x1b[2K = erase entire line, \r = carriage return.
            print(f"\r\x1b[2K{line}", end="", file=self._stream, flush=True)
            self._last_line_len = max(self._last_line_len, len(line))

    def finish(self, line: str) -> None:
        """Finalize the current phase line (prints newline)."""
        with self._lock:
            if self._is_tty:
                print(f"\r\x1b[2K{line}", file=self._stream, flush=True)
                self._last_line_len = 0
            else:
                print(line, file=self._stream, flush=True)


def parse_args(
    pdf_path: str,
    output_dir: str,
    parse_only: bool = False,
    from_parse: Optional[str] = None,
) -> tuple[str, Path, bool, Optional[str]]:
    """Parse and validate arguments."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    return pdf_path, output_path, parse_only, from_parse


def phase1_parse_pdf(
    pdf_path: str, output_dir: Path, overwrite: bool = False
) -> Path:
    """
    Phase 1: Parse PDF and generate intermediate output.
    
    - Extract embedded images from each page
    - Render each page as a complete PNG image (using page number as filename suffix)

    Returns:
        Path to the generated parse_result.json file
    """
    progress = _ProgressPrinter(sys.stderr)

    # Open PDF
    t0 = time.monotonic()
    doc = open_pdf(pdf_path)
    total_pages = len(doc)
    progress.finish(f"[1/5] Open PDF: done ({total_pages} pages, {_format_duration(time.monotonic() - t0)})")

    try:
        # Render each page as PNG image
        t_render = time.monotonic()
        page_images = []
        last_update = 0.0
        for page_index in range(total_pages):
            now = time.monotonic()
            if now - last_update >= _PROGRESS_UPDATE_INTERVAL_SEC or page_index + 1 == total_pages:
                progress.update(f"[2/5] Render pages: {page_index + 1}/{total_pages}")
                last_update = now

            page = doc[page_index]
            image_bytes, image_meta = render_page_as_image(page)
            
            # Generate filename with page number suffix
            filename = generate_page_image_filename(page_index, "png")
            image_path = save_image(image_bytes, output_dir, filename, overwrite=overwrite)
            
            page_images.append(
                {
                    "page_index": page_index,
                    "type": "page_image",
                    "imagePath": str(image_path),
                    "ext": image_meta.get("ext"),
                    "width": image_meta.get("width"),
                    "height": image_meta.get("height"),
                }
            )
        progress.finish(
            f"[2/5] Render pages: done ({total_pages}/{total_pages}, {_format_duration(time.monotonic() - t_render)})"
        )

        # Parse PDF to get embedded image blocks
        t_scan = time.monotonic()
        scan_last_update = 0.0

        def _scan_progress(cur: int, total: int) -> None:
            nonlocal scan_last_update
            now = time.monotonic()
            if now - scan_last_update >= _PROGRESS_UPDATE_INTERVAL_SEC or cur == total:
                progress.update(f"[3/5] Scan embedded images: {cur}/{total}")
                scan_last_update = now

        blocks = parse_pdf(doc, progress_cb=_scan_progress)
        progress.finish(
            f"[3/5] Scan embedded images: done ({total_pages}/{total_pages}, {_format_duration(time.monotonic() - t_scan)})"
        )

        # Process embedded image blocks
        t_extract = time.monotonic()
        total_blocks = len(blocks)
        extract_last_update = 0.0
        for idx, block in enumerate(blocks):
            now = time.monotonic()
            if now - extract_last_update >= _PROGRESS_UPDATE_INTERVAL_SEC or idx + 1 == total_blocks:
                progress.update(f"[4/5] Extract embedded images: {idx + 1}/{total_blocks}")
                extract_last_update = now

            if block.get("type") == "image":
                # Extract embedded image
                xref = block.get("xref")
                if xref is not None:
                    image_bytes, image_meta = extract_image(doc, int(xref))

                    # Generate filename and save
                    ext = image_meta.get("ext", "png")
                    filename = generate_image_filename(ext)
                    image_path = save_image(image_bytes, output_dir, filename, overwrite=overwrite)

                    # Update block with image metadata
                    block["imagePath"] = str(image_path)
                    block["ext"] = image_meta.get("ext")
                    block["width"] = image_meta.get("width")
                    block["height"] = image_meta.get("height")
        progress.finish(
            f"[4/5] Extract embedded images: done ({total_blocks}/{total_blocks}, {_format_duration(time.monotonic() - t_extract)})"
        )

        # Combine page images and embedded images
        all_blocks = page_images + blocks
        
        # Re-sort and re-index all blocks
        def sort_key(block: Dict[str, Any]) -> tuple:
            if block.get("type") == "page_image":
                # Page images come first, sorted by page_index
                return (0, block.get("page_index", 0))
            else:
                # Embedded images sorted by page_index -> bbox.y -> bbox.x
                page_idx = block.get("page_index", 0)
                bbox = block.get("bbox", [0, 0, 0, 0])
                y = bbox[1] if len(bbox) > 1 else 0.0
                x = bbox[0] if len(bbox) > 0 else 0.0
                return (1, page_idx, y, x)
        
        all_blocks.sort(key=sort_key)
        
        # Add blockIndex
        for index, block in enumerate(all_blocks):
            block["blockIndex"] = index

        # Create parse result structure
        t_save = time.monotonic()
        parse_result = create_parse_result(
            source_pdf=pdf_path, total_pages=total_pages, blocks=all_blocks
        )

        # Save parse result
        parse_output_path = save_parse_result(parse_result, output_dir, overwrite=overwrite)
        progress.finish(f"[5/5] Save parse result: done ({_format_duration(time.monotonic() - t_save)})")

        return parse_output_path

    finally:
        doc.close()


def _load_prompt_template(prompt_path: Path) -> str:
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    if not prompt_path.is_file():
        raise ValueError(f"Prompt path is not a file: {prompt_path}")
    content = prompt_path.read_text(encoding="utf-8")
    if not content.strip():
        raise ValueError(f"Prompt file is empty: {prompt_path}")
    return content


def _iter_page_blocks(
    parse_result: Dict[str, Any], page_index: int
) -> Iterable[Dict[str, Any]]:
    for block in parse_result.get("blocks", []):
        if block.get("page_index") == page_index:
            yield block


def _build_pages_input(
    *, parse_result: Dict[str, Any], output_dir: Path
) -> List[Dict[str, Any]]:
    total_pages = int(parse_result.get("total_pages", 0))
    pages: List[Dict[str, Any]] = []

    for page_index in range(total_pages):
        blocks = list(_iter_page_blocks(parse_result, page_index))

        page_image_blocks = [b for b in blocks if b.get("type") == "page_image"]
        if not page_image_blocks:
            raise ValueError(f"Missing page_image block for page_index={page_index}")
        page_image = page_image_blocks[0]

        page_image_rel = Path(str(page_image.get("imagePath", "")))
        if not page_image_rel.as_posix():
            raise ValueError(f"Missing page_image imagePath for page_index={page_index}")
        page_image_abs = output_dir / page_image_rel
        if not page_image_abs.exists():
            raise FileNotFoundError(f"Page image file not found: {page_image_abs}")

        embedded_blocks = [b for b in blocks if b.get("type") == "image"]
        embedded_images_meta: List[Dict[str, Any]] = []
        for b in embedded_blocks:
            embedded_images_meta.append(
                {
                    "imagePath": b.get("imagePath"),
                    "bbox": b.get("bbox"),
                    "xref": b.get("xref"),
                    "ext": b.get("ext"),
                    "width": b.get("width"),
                    "height": b.get("height"),
                }
            )

        page_parse_dict = {
            "page_index": page_index,
            "blocks": blocks,
        }

        pages.append(
            {
                "page_index": page_index,
                "page_image_rel": page_image_rel.as_posix(),
                "page_image_abs": page_image_abs,
                "embedded_images_meta": embedded_images_meta,
                "page_parse_dict": page_parse_dict,
            }
        )

    return pages


def _build_page_prompt(
    *,
    prompt_template_md: str,
    page_index: int,
    page_image_rel: str,
    embedded_images_meta: List[Dict[str, Any]],
    page_parse_dict: Dict[str, Any],
) -> str:
    appended = {
        "page_index": page_index,
        "page_image_path": page_image_rel,
        "embedded_images_meta": embedded_images_meta,
        "page_parse_dict": page_parse_dict,
    }
    return (
        prompt_template_md.rstrip()
        + "\n\n---\n\n"
        + "## 參考資料（程式自動附加）\n\n"
        + "以下 JSON 是本頁的結構化參考資料。請用來輔助理解，但不要原樣貼回輸出。\n\n"
        + json.dumps(appended, ensure_ascii=False, indent=2)
        + "\n"
    )


def _build_recitation_safe_prompt(prompt_text: str) -> str:
    """Build a fallback prompt when the model blocks output with RECITATION."""
    return (
        prompt_text.rstrip()
        + "\n\n---\n\n"
        + "## 安全模式（避免逐字轉錄 / RECITATION）\n\n"
        + "- 禁止逐字轉錄：不得連續輸出長句原文。\n"
        + "- 請改用「提要式結構化整理」：保留標題/段落結構，但每段只輸出 3–8 個重點 bullet。\n"
        + "- 必須保留關鍵資訊：數字門檻、日期、專有名詞、網址、表格欄位名稱。\n"
        + "- 如需引用原詞句，只能用短語（8–12 字）且不可連續多句。\n"
        + "- 請仍然正確引用圖片路徑（images/...)。\n"
    )


def _is_recitation_error(err: Exception) -> bool:
    msg = str(err)
    return ("FinishReason.RECITATION" in msg) or ("RECITATION" in msg)


def _save_markdown(output_dir: Path, markdown: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = output_dir / f"output_{timestamp}.md"
    out_path.write_text(markdown, encoding="utf-8")
    return out_path


def _phase2_dir(output_dir: Path) -> Path:
    d = output_dir / "phase2"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _phase2_pages_dir(output_dir: Path) -> Path:
    d = _phase2_dir(output_dir) / "pages"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _phase2_state_path(output_dir: Path) -> Path:
    return _phase2_dir(output_dir) / "state.json"


def _file_fingerprint(path: Path) -> dict[str, int]:
    st = path.stat()
    return {"size": int(st.st_size), "mtime_ns": int(st.st_mtime_ns)}


def _text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _load_phase2_state(output_dir: Path) -> Dict[str, Any]:
    state_path = _phase2_state_path(output_dir)
    if not state_path.exists():
        return {}
    try:
        return json.loads(state_path.read_text(encoding="utf-8"))
    except Exception:  # pylint: disable=broad-exception-caught
        # If state is corrupted, ignore it rather than blocking conversions.
        return {}


def _save_phase2_state(output_dir: Path, state: Dict[str, Any]) -> None:
    state_path = _phase2_state_path(output_dir)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _phase2_page_md_path(output_dir: Path, page_index: int) -> Path:
    return _phase2_pages_dir(output_dir) / f"page_{page_index:04d}.md"


def _rebuild_completed_pages_from_disk(output_dir: Path) -> Dict[str, Any]:
    """Rebuild completed_pages map from existing per-page markdown files.

    This makes resume robust even if state.json is missing/corrupted or identity changes.
    """
    completed: Dict[str, Any] = {}
    pages_dir = _phase2_pages_dir(output_dir)
    for p in sorted(pages_dir.glob("page_*.md")):
        stem = p.stem  # page_0000
        try:
            page_index = int(stem.split("_", 1)[1])
        except Exception:  # pylint: disable=broad-exception-caught
            continue
        rel = p.relative_to(output_dir)
        completed[str(page_index)] = {
            "path": str(rel),
            "bytes": int(p.stat().st_size),
        }
    return completed


def _process_single_page(
    page: Dict[str, Any],
    idx: int,
    total_pages: int,
    output_dir: Path,
    state: Dict[str, Any],
    state_lock: threading.Lock,
    model: str,
    prompt_template_md: str,
    progress: _ProgressPrinter,
) -> str:
    """Process a single page: cache check -> generate -> save."""
    page_no = idx + 1
    page_index = int(page["page_index"])
    t_page0 = time.monotonic()
    embedded_count = len(page["embedded_images_meta"])

    # If cached on disk, read and reuse immediately (disk is source of truth).
    # We need to access state["completed_pages"] which is shared.
    with state_lock:
        completed_pages: Dict[str, Any] = state.get("completed_pages", {})
    
    page_md_path = _phase2_page_md_path(output_dir, page_index)
    
    if page_md_path.exists():
        # Ensure state reflects reality (in case it was missing/corrupted).
        with state_lock:
            state.setdefault("completed_pages", {})[str(page_index)] = {
                "path": str(page_md_path.relative_to(output_dir)),
                "bytes": int(page_md_path.stat().st_size),
            }
        
        progress.finish(
            f"[Phase 2] Page {page_no}/{total_pages}: cache hit "
            f"(page_index={page_index}, path={page_md_path.relative_to(output_dir)})"
        )
        return page_md_path.read_text(encoding="utf-8")

    progress.update(
        f"[Phase 2] Page {page_no}/{total_pages}: 準備本頁資料（embedded={embedded_count}, image={page['page_image_rel']}）"
    )
    t_prepare = time.monotonic()
    # (目前 prepare 主要是組合資料與前置檢查；避免在進度停住時看不出在做什麼)
    dt_prepare = time.monotonic() - t_prepare

    page_md = ""
    dt_prompt = 0.0
    dt_gemini = 0.0
    dt_gemini_retry = 0.0
    t_gemini: float | None = None
    try:
        progress.update(
            f"[Phase 2] Page {page_no}/{total_pages}: 建立 prompt…"
        )
        t_prompt = time.monotonic()
        prompt_text = _build_page_prompt(
            prompt_template_md=prompt_template_md,
            page_index=page["page_index"],
            page_image_rel=page["page_image_rel"],
            embedded_images_meta=page["embedded_images_meta"],
            page_parse_dict=page["page_parse_dict"],
        )
        dt_prompt = time.monotonic() - t_prompt
        progress.update(
            f"[Phase 2] Page {page_no}/{total_pages}: 建立 prompt: done（{_format_duration(dt_prompt)}）"
        )

        progress.update(
            f"[Phase 2] Page {page_no}/{total_pages}: 等待 Gemini 回應…（model={model}）"
        )
        t_gemini = time.monotonic()
        try:
            page_md = generate_page_markdown(
                prompt_text=prompt_text,
                page_image_path=page["page_image_abs"],
                model=model,
            )
            dt_gemini = time.monotonic() - t_gemini
        except Exception as e:  # pylint: disable=broad-exception-caught
            # Capture time spent waiting for Gemini even when it errors.
            dt_gemini = time.monotonic() - t_gemini

            # If the model blocks with RECITATION, retry once with a safer prompt.
            if _is_recitation_error(e):
                progress.finish(
                    f"[Phase 2] Page {page_no}/{total_pages}: 觸發 RECITATION，改用安全模式重試一次"
                )
                safe_prompt_text = _build_recitation_safe_prompt(prompt_text)
                progress.update(
                    f"[Phase 2] Page {page_no}/{total_pages}: 等待 Gemini 回應（安全模式）…（model={model}）"
                )
                t_retry = time.monotonic()
                page_md = generate_page_markdown(
                    prompt_text=safe_prompt_text,
                    page_image_path=page["page_image_abs"],
                    model=model,
                )
                dt_gemini_retry = time.monotonic() - t_retry
            else:
                raise
    except Exception as e:  # pylint: disable=broad-exception-caught
        dt_total = time.monotonic() - t_page0
        progress.finish(
            "[Phase 2] "
            f"Page {page_no}/{total_pages}: ERROR "
            f"(page_index={page_index}, "
            f"image={page['page_image_rel']}, "
            f"embedded={embedded_count}, "
            f"prepare={_format_duration(dt_prepare)}, "
            f"prompt={_format_duration(dt_prompt)}, "
            f"gemini={_format_duration(dt_gemini)}, "
            f"gemini_retry={_format_duration(dt_gemini_retry)}, "
            f"total={_format_duration(dt_total)})"
        )
        # Raise a context-rich error so CLI prints something actionable.
        extra_hint = ""
        msg = str(e)
        if "FinishReason.RECITATION" in msg or "RECITATION" in msg:
            extra_hint = (
                " Hint: finish_reason=RECITATION 通常代表模型認為輸出會接近逐字轉錄/版權內容而拒絕；"
                "可嘗試調整 prompt 讓輸出改為摘要/改寫而非逐字還原。"
            )
        raise RuntimeError(
            "Phase 2 failed while converting a page. "
            f"page={page_no}/{total_pages} (page_index={page_index}), "
            f"image={page['page_image_rel']}, "
            f"embedded={embedded_count}, "
            f"model={model}. "
            f"Cause: {e}.{extra_hint}"
        ) from e

    dt_total = time.monotonic() - t_page0
    progress.finish(
        "[Phase 2] "
        f"Page {page_no}/{total_pages}: done "
        f"(prepare={_format_duration(dt_prepare)}, "
        f"prompt={_format_duration(dt_prompt)}, "
        f"gemini={_format_duration(dt_gemini)}, "
        f"gemini_retry={_format_duration(dt_gemini_retry)}, "
        f"total={_format_duration(dt_total)}, "
        f"md_chars={len(page_md)})"
    )
    
    # Persist per-page output + state for resume
    page_md_path.write_text(page_md.strip() + "\n", encoding="utf-8")
    
    with state_lock:
        state.setdefault("completed_pages", {})[str(page_index)] = {
            "path": str(page_md_path.relative_to(output_dir)),
            "md_chars": len(page_md),
            "bytes": int(page_md_path.stat().st_size),
        }
        _save_phase2_state(output_dir, state)

    return page_md.strip()


def convert_to_markdown(
    parse_input_path: str, output_dir: Path, model: str, prompt_file: str
) -> Path:
    """
    Phase 2: Convert parse result to Markdown.

    Args:
        parse_input_path: Path to parse result JSON file
        output_dir: Output directory containing images/
        model: AI model name
        prompt_file: Prompt template markdown file path
    """
    # Load parse result
    parse_result = load_parse_result(Path(parse_input_path))

    # Validate schema version
    if not validate_schema_version(parse_result):
        raise ValueError(
            f"Unsupported schema version: {parse_result.get('schema_version')}"
        )

    # Validate block index order
    if not validate_block_index_order(parse_result):
        raise ValueError("Block index order is invalid or incomplete")

    prompt_template_md = _load_prompt_template(Path(prompt_file))

    pages = _build_pages_input(parse_result=parse_result, output_dir=output_dir)

    # Resume support: save each page as it completes, and skip already-done pages
    parse_path = Path(parse_input_path).resolve()
    prompt_path = Path(prompt_file).resolve()
    state = _load_phase2_state(output_dir)

    desired_state_identity = {
        "parse_input_path": str(parse_path),
        "parse_input_fingerprint": _file_fingerprint(parse_path),
        "prompt_file": str(prompt_path),
        "prompt_sha256": _text_sha256(prompt_template_md),
        "model": model,
        "total_pages": len(pages),
        "schema_version": parse_result.get("schema_version"),
    }

    # If the existing state does not match current inputs, start a fresh identity
    # but KEEP already generated per-page outputs by rebuilding from disk.
    if state.get("identity") != desired_state_identity:
        state = {
            "identity": desired_state_identity,
            "created_at": datetime.now().isoformat(),
            "completed_pages": _rebuild_completed_pages_from_disk(output_dir),
        }
        _save_phase2_state(output_dir, state)

    progress = _ProgressPrinter(sys.stderr)
    t0 = time.monotonic()
    
    # Configuration for concurrency
    concurrency = int(os.getenv("GEMINI_CONCURRENCY", "10"))
    if concurrency < 1:
        concurrency = 1
    
    total_pages = len(pages)
    progress.finish(f"[Phase 2] Starting conversion with concurrency={concurrency}")
    
    # Store results by page_index to sort later
    results: Dict[int, str] = {}
    state_lock = threading.Lock()
    
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        future_to_page = {
            executor.submit(
                _process_single_page,
                page=page,
                idx=idx,
                total_pages=total_pages,
                output_dir=output_dir,
                state=state,
                state_lock=state_lock,
                model=model,
                prompt_template_md=prompt_template_md,
                progress=progress,
            ): idx
            for idx, page in enumerate(pages)
        }
        
        for future in as_completed(future_to_page):
            idx = future_to_page[future]
            try:
                page_md = future.result()
                results[idx] = page_md
            except Exception as e:
                # If any page fails, we should probably stop or at least log it.
                # For now, we let the exception bubble up, which stops the main thread 
                # (but other threads might continue briefly).
                # raise RuntimeError(f"Failed to process page index {idx}") from e
                raise

    progress.finish(
        f"[Phase 2] Convert pages: done ({total_pages}/{total_pages}, {_format_duration(time.monotonic() - t0)})"
    )

    # Sort results by index to ensure correct order
    sorted_mds = [results[i] for i in range(total_pages)]
    combined_md = ("\n\n---\n\n".join(sorted_mds)).rstrip() + "\n"
    return _save_markdown(output_dir, combined_md)
