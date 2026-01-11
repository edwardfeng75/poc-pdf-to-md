# PDF to Markdown Tool

[中文說明](README_zhtw.md)

A PDF to Markdown tool with image extraction and AI-assisted conversion. It uses PyMuPDF for PDF parsing and is designed as a two-phase pipeline to keep outputs inspectable and reproducible.

## Features

- **PDF Parsing**: Extract text and images using PyMuPDF
- **Image Extraction**: Automatically extract and save images
- **AI Conversion**: Convert text to Markdown using Gemini AI
- **Thinking Mode**: Support for Gemini's thinking capability (via env var) for better reasoning on complex content
- **Auto-Retry**: Automatically fallback to safe mode on Recitation Error to ensure high success rate
- **Two-Phase Pipeline**: Separate parsing and conversion for quality assurance

## Project Status

- **Phase 1**: PDF parsing + inspectable intermediate output (done)
- **Phase 2**: Convert parse output to Markdown (done)

## Requirements

- Python >= 3.14.0
- uv (Python package manager)

## Setup

### Install dependencies

```bash
uv sync
```

### Environment variables (Phase 2)

Phase 1 does not require API keys. Phase 2 requires them.

```bash
cp .env.example .env
```

```bash
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3-pro-preview
GEMINI_CONCURRENCY=10 # Optional: Phase 2 concurrency (default: 10)
GEMINI_ENABLE_THINKING=true # Optional: Enable Thinking Mode (default: False, for models that support it)
```

## Usage (uv)

### Help

```bash
uv run poc-pdf-to-md --help
```

### Phase 1: Parse PDF (parse only)

```bash
uv run poc-pdf-to-md --input <path-to-pdf> --parse-only
```

Example:

```bash
uv run poc-pdf-to-md --input test_data/test_data.pdf --parse-only
```

### Phase 2: Convert from parse result

```bash
uv run poc-pdf-to-md --from-parse <path-to-parse_result.json>
```

## CLI Arguments

| Argument | Description | Required | Default |
|---|---|---:|---|
| `--input <path>` | PDF file path (required unless `--from-parse` is provided) | Conditional | - |
| `--output <dir>` | Output directory | No | `output/` |
| `--parse-only` | Run Phase 1 only (parse, do not convert) | No | `false` |
| `--from-parse <path>` | Convert from an existing parse result JSON | No | - |
| `--model <name>` | AI model name (priority: `--model` > `GEMINI_MODEL` > default) | No | `gemini-3-pro-preview` |
| `--prompt-file <path>` | Prompt template markdown file for Phase 2 | No | `prompts/phase2_page_to_md.md` |
| `--overwrite` | Overwrite existing output files (clears `parsed/`, `images/`, `logs/`, and `output_*.md`) | No | `false` |

## Output Structure

The tool generates the following structure in the output directory:

```
output/
├── parsed/
│   └── parse_result_<timestamp>.json  # Parse result JSON
├── images/
│   ├── page_0000.png                  # Page renders
│   └── <uuid>.png                     # Extracted images
├── phase2/
│   ├── pages/                         # Intermediate Markdown per page
│   │   └── page_0000.md
│   └── state.json                     # Resume state file
└── output_<timestamp>.md              # Final combined Markdown file
```

## Running tests

```bash
uv run pytest tests/ -v
```
