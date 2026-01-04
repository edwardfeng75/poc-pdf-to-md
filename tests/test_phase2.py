"""Tests for Phase 2 conversion (parse_result -> Markdown)."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from poc_pdf_to_md.engine import convert_to_markdown


def _write_dummy_png(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Minimal bytes; Phase 2 only checks file existence (AI call is mocked).
    path.write_bytes(b"\x89PNG\r\n\x1a\n")


class TestPhase2ConvertToMarkdown:
    temp_dir: Path
    prompt_file: Path
    parse_file: Path

    def setup_method(self):
        self.temp_dir = Path(tempfile.mkdtemp())

        # Create images referenced by parse_result
        _write_dummy_png(self.temp_dir / "images" / "page_0000.png")
        _write_dummy_png(self.temp_dir / "images" / "page_0001.png")
        (self.temp_dir / "images" / "img_page0.png").write_bytes(b"img0")
        (self.temp_dir / "images" / "img_page1.jpg").write_bytes(b"img1")

        # Prompt file
        self.prompt_file = self.temp_dir / "prompt.md"
        self.prompt_file.write_text("請把本頁轉成 Markdown。", encoding="utf-8")

        # Parse result with 2 pages, sequential blockIndex
        self.parse_file = self.temp_dir / "parsed" / "parse_result.json"
        self.parse_file.parent.mkdir(parents=True, exist_ok=True)
        self.parse_file.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "created_at": "2026-01-01T00:00:00Z",
                    "source_pdf": "test.pdf",
                    "total_pages": 2,
                    "blocks": [
                        {
                            "blockIndex": 0,
                            "page_index": 0,
                            "type": "page_image",
                            "imagePath": "images/page_0000.png",
                            "ext": "png",
                            "width": 100,
                            "height": 200,
                        },
                        {
                            "blockIndex": 1,
                            "page_index": 1,
                            "type": "page_image",
                            "imagePath": "images/page_0001.png",
                            "ext": "png",
                            "width": 100,
                            "height": 200,
                        },
                        {
                            "blockIndex": 2,
                            "page_index": 0,
                            "type": "image",
                            "imagePath": "images/img_page0.png",
                            "bbox": [1, 2, 3, 4],
                            "xref": 111,
                            "ext": "png",
                            "width": 10,
                            "height": 20,
                        },
                        {
                            "blockIndex": 3,
                            "page_index": 1,
                            "type": "image",
                            "imagePath": "images/img_page1.jpg",
                            "bbox": [5, 6, 7, 8],
                            "xref": 222,
                            "ext": "jpg",
                            "width": 30,
                            "height": 40,
                        },
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    def teardown_method(self):
        import shutil

        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_phase2_generates_output_markdown_and_calls_ai_per_page(self):
        prompts: list[str] = []

        def _mock_generate_page_markdown(*, prompt_text, page_image_path, model, generation_config=None):
            _ = generation_config
            assert page_image_path.exists()
            assert model == "test-model"
            prompts.append(prompt_text)
            return f"## page\n\n![]({page_image_path.name})"

        with patch("poc_pdf_to_md.engine.generate_page_markdown", side_effect=_mock_generate_page_markdown) as mock_ai:
            out_path = convert_to_markdown(
                str(self.parse_file),
                self.temp_dir,
                "test-model",
                str(self.prompt_file),
            )

        assert out_path.exists()
        assert out_path.name.startswith("output_")
        assert out_path.suffix == ".md"
        assert mock_ai.call_count == 2
        # per-page md should be persisted for resume
        assert (self.temp_dir / "phase2" / "pages" / "page_0000.md").exists()
        assert (self.temp_dir / "phase2" / "pages" / "page_0001.md").exists()
        assert (self.temp_dir / "phase2" / "state.json").exists()

        content = out_path.read_text(encoding="utf-8")
        assert "---" in content  # page separator
        assert content.strip().startswith("## page")

        # Ensure each prompt contains its page_index and correct embedded images meta
        # Sort prompts by page_index to ensure deterministic checking
        prompt_data = []
        for p in prompts:
            data = json.loads(p[p.index("{") :])
            prompt_data.append(data)
        
        prompt_data.sort(key=lambda x: x["page_index"])
        
        data0 = prompt_data[0]
        data1 = prompt_data[1]
        assert data0["page_index"] == 0
        assert data1["page_index"] == 1
        assert data0["page_image_path"] == "images/page_0000.png"
        assert data1["page_image_path"] == "images/page_0001.png"
        assert any(m["imagePath"] == "images/img_page0.png" for m in data0["embedded_images_meta"])
        assert all(m["imagePath"] != "images/img_page1.jpg" for m in data0["embedded_images_meta"])

    def test_phase2_missing_prompt_file_raises(self):
        with pytest.raises(FileNotFoundError):
            convert_to_markdown(
                str(self.parse_file),
                self.temp_dir,
                "test-model",
                str(self.temp_dir / "missing.md"),
            )

    def test_phase2_empty_prompt_file_raises(self):
        empty_prompt = self.temp_dir / "empty.md"
        empty_prompt.write_text("", encoding="utf-8")
        with pytest.raises(ValueError, match="Prompt file is empty"):
            convert_to_markdown(
                str(self.parse_file),
                self.temp_dir,
                "test-model",
                str(empty_prompt),
            )

    def test_phase2_ai_error_includes_page_context(self):
        def _mock_generate_page_markdown(*, prompt_text, page_image_path, model, generation_config=None):
            _ = (prompt_text, page_image_path, model, generation_config)
            raise RuntimeError("Gemini returned an empty response (missing response.text).")

        with patch("poc_pdf_to_md.engine.generate_page_markdown", side_effect=_mock_generate_page_markdown):
            with pytest.raises(RuntimeError) as excinfo:
                convert_to_markdown(
                    str(self.parse_file),
                    self.temp_dir,
                    "test-model",
                    str(self.prompt_file),
                )
            msg = str(excinfo.value)
            assert "Phase 2 failed while converting a page" in msg or "Failed to process page index" in msg
            # The exact page index might vary depending on which thread fails first in parallel execution
            assert "page=" in msg or "page_index=" in msg

    def test_phase2_resume_skips_completed_pages(self):
        # First run populates cache
        def _mock_generate_page_markdown(*, prompt_text, page_image_path, model, generation_config=None):
            _ = (prompt_text, page_image_path, model, generation_config)
            return f"page for {page_image_path.name}"

        with patch("poc_pdf_to_md.engine.generate_page_markdown", side_effect=_mock_generate_page_markdown) as mock_ai:
            convert_to_markdown(
                str(self.parse_file),
                self.temp_dir,
                "test-model",
                str(self.prompt_file),
            )
        assert mock_ai.call_count == 2

        # Second run should not call AI at all (cache hit)
        with patch("poc_pdf_to_md.engine.generate_page_markdown") as mock_ai2:
            convert_to_markdown(
                str(self.parse_file),
                self.temp_dir,
                "test-model",
                str(self.prompt_file),
            )
        assert mock_ai2.call_count == 0

    def test_phase2_resume_survives_prompt_change_via_disk_cache(self):
        # First run creates per-page files
        def _mock_generate_page_markdown(*, prompt_text, page_image_path, model, generation_config=None):
            _ = (prompt_text, model, generation_config)
            return f"page for {page_image_path.name}"

        with patch("poc_pdf_to_md.engine.generate_page_markdown", side_effect=_mock_generate_page_markdown):
            convert_to_markdown(
                str(self.parse_file),
                self.temp_dir,
                "test-model",
                str(self.prompt_file),
            )

        # Change prompt (would previously invalidate identity and reset state)
        self.prompt_file.write_text("changed prompt", encoding="utf-8")

        # Should still skip because per-page files exist (disk is source of truth)
        with patch("poc_pdf_to_md.engine.generate_page_markdown") as mock_ai:
            convert_to_markdown(
                str(self.parse_file),
                self.temp_dir,
                "test-model",
                str(self.prompt_file),
            )
        assert mock_ai.call_count == 0

    def test_phase2_recitation_retries_with_safe_prompt(self):
        calls: list[str] = []

        def _mock_generate_page_markdown(*, prompt_text, page_image_path, model, generation_config=None):
            _ = (page_image_path, model, generation_config)
            calls.append(prompt_text)
            if len(calls) == 1:
                raise RuntimeError("FinishReason.RECITATION")
            return "ok"

        # Use a fresh temp dir so cache doesn't skip calls
        tmp = Path(tempfile.mkdtemp())
        try:
            # Copy minimal setup from existing fixture
            _write_dummy_png(tmp / "images" / "page_0000.png")
            _write_dummy_png(tmp / "images" / "page_0001.png")
            (tmp / "images" / "img_page0.png").write_bytes(b"img0")
            (tmp / "images" / "img_page1.jpg").write_bytes(b"img1")
            prompt_file = tmp / "prompt.md"
            prompt_file.write_text("prompt", encoding="utf-8")
            parse_file = tmp / "parsed" / "parse_result.json"
            parse_file.parent.mkdir(parents=True, exist_ok=True)
            parse_file.write_text(self.parse_file.read_text(encoding="utf-8"), encoding="utf-8")

            with patch("poc_pdf_to_md.engine.generate_page_markdown", side_effect=_mock_generate_page_markdown):
                convert_to_markdown(
                    str(parse_file),
                    tmp,
                    "test-model",
                    str(prompt_file),
                )

            assert len(calls) >= 2
            # Parallel execution order is not guaranteed, so check if any call contains safe prompt
            assert any("安全模式" in c for c in calls)
        finally:
            import shutil
            shutil.rmtree(tmp)

