"""Gemini client wrapper for multimodal page-to-Markdown conversion.

This module is intentionally thin so it can be easily mocked in tests.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv


def _get_api_key() -> str:
    # Load .env if present (safe no-op if not).
    load_dotenv()
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""


def _summarize_genai_response(resp: Any) -> str:
    """Return a short, safe diagnostic summary for debugging."""
    parts: list[str] = [f"response_type={type(resp).__name__}"]

    usage = getattr(resp, "usage_metadata", None)
    if usage is not None:
        total = getattr(usage, "total_token_count", None)
        prompt = getattr(usage, "prompt_token_count", None)
        cand = getattr(usage, "candidates_token_count", None)
        if total is not None or prompt is not None or cand is not None:
            parts.append(
                f"tokens(total={total}, prompt={prompt}, candidates={cand})"
            )

    candidates = getattr(resp, "candidates", None)
    if candidates is not None:
        try:
            parts.append(f"candidates={len(candidates)}")
            finish_reasons: list[str] = []
            for c in candidates[:3]:
                fr = getattr(c, "finish_reason", None)
                if fr is not None:
                    finish_reasons.append(str(fr))
            if finish_reasons:
                parts.append(f"finish_reason={finish_reasons}")
        except Exception:  # pylint: disable=broad-exception-caught
            parts.append("candidates=<unreadable>")

    prompt_feedback = getattr(resp, "prompt_feedback", None)
    if prompt_feedback is not None:
        try:
            parts.append(f"prompt_feedback={prompt_feedback}")
        except Exception:  # pylint: disable=broad-exception-caught
            parts.append("prompt_feedback=<unreadable>")

    return ", ".join(parts)


def generate_page_markdown(
    *,
    prompt_text: str,
    page_image_path: Path,
    model: str,
    generation_config: Dict[str, Any] | None = None,
) -> str:
    """Generate Markdown for a single page using Gemini (multimodal).

    Args:
        prompt_text: Final prompt text (already includes page context).
        page_image_path: Absolute path to the page PNG.
        model: Gemini model name.
        generation_config: Optional model generation config.
    """
    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError(
            "Missing API key. Set GEMINI_API_KEY (preferred) or GOOGLE_API_KEY."
        )

    # Use the new SDK: google-genai (import path: google.genai).
    from google import genai  # type: ignore[import-not-found]
    from google.genai import types  # type: ignore[import-not-found]

    client = genai.Client(api_key=api_key)

    image_bytes = page_image_path.read_bytes()
    image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/png")

    kwargs: Dict[str, Any] = {}
    if generation_config is not None:
        kwargs["config"] = generation_config

    resp = client.models.generate_content(
        model=model,
        contents=[prompt_text, image_part],
        **kwargs,
    )

    # Best-effort extraction across SDK versions.
    text = getattr(resp, "text", None)
    if isinstance(text, str) and text.strip():
        return text

    summary = _summarize_genai_response(resp)
    raise RuntimeError(
        "Gemini returned an empty response (missing response.text). "
        f"Diagnostics: {summary}"
    )

