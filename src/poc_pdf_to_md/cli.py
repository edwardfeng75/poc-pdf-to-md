"""CLI interface for PDF to Markdown converter."""

import argparse
import os
import sys
from pathlib import Path

from .engine import phase1_parse_pdf, convert_to_markdown


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Convert PDF to Markdown with image extraction and AI assistance"
    )
    parser.add_argument(
        "--input",
        type=str,
        required=False,
        default=None,
        help="PDF file path (required unless --from-parse is provided)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="Output directory (default: output/)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="AI model name (priority: --model > GEMINI_MODEL env > default)",
    )
    parser.add_argument(
        "--parse-only",
        action="store_true",
        help="Only output PDF parsing results, do not convert (mutually exclusive with --from-parse)",
    )
    parser.add_argument(
        "--from-parse",
        type=str,
        default=None,
        help="Use parsed output as input for conversion (mutually exclusive with --parse-only)",
    )
    parser.add_argument(
        "--prompt-file",
        type=str,
        default="prompts/phase2_page_to_md.md",
        help="Prompt template markdown file for Phase 2 (default: prompts/phase2_page_to_md.md)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="Overwrite existing files in output directory (default: False, AI development should enable this)",
    )

    args = parser.parse_args()

    # Validate mutual exclusivity
    if args.parse_only and args.from_parse:
        print(
            "Error: --parse-only and --from-parse cannot be used together",
            file=sys.stderr,
        )
        sys.exit(1)

    # Validate input is provided and exists (only if not using --from-parse)
    if not args.from_parse:
        if not args.input:
            print(
                "Error: --input is required unless --from-parse is provided",
                file=sys.stderr,
            )
            sys.exit(1)

        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: PDF file not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        if not input_path.is_file():
            print(f"Error: Input path is not a file: {args.input}", file=sys.stderr)
            sys.exit(1)

    # Validate --from-parse file exists
    if args.from_parse:
        parse_path = Path(args.from_parse)
        if not parse_path.exists():
            print(
                f"Error: Parse result file not found: {args.from_parse}",
                file=sys.stderr,
            )
            sys.exit(1)
        if not parse_path.is_file():
            print(
                f"Error: Parse result path is not a file: {args.from_parse}",
                file=sys.stderr,
            )
            sys.exit(1)

    return args


def get_model_name(args: argparse.Namespace) -> str:
    """Get model name with priority: --model > GEMINI_MODEL env > default."""
    if args.model:
        return args.model
    env_model = os.getenv("GEMINI_MODEL")
    if env_model:
        return env_model
    return "gemini-3-pro-preview"


def print_parse_output_path(parse_output_path: str) -> None:
    """Print parse output path to user."""
    print(f"Parse output saved to: {parse_output_path}")
    print("Please review the parsing results before proceeding to Phase 2.")


def print_success_message(
    output_md_path: str, images_dir: str, logs_dir: str
) -> None:
    """Print success message with output paths."""
    print("Conversion completed successfully!")
    print(f"Markdown output: {output_md_path}")
    print(f"Images directory: {images_dir}")
    print(f"Logs directory: {logs_dir}")


def main() -> None:
    """Main entry point for PDF to Markdown converter."""
    args = parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Handle overwrite flag
    if args.overwrite:
        # Clear existing output directories
        import shutil
        for subdir in ["parsed", "images", "logs"]:
            subdir_path = output_dir / subdir
            if subdir_path.exists():
                shutil.rmtree(subdir_path)
        # Remove existing markdown files
        for md_file in output_dir.glob("output_*.md"):
            md_file.unlink()

    if args.parse_only:
        # Phase 1 only: Parse PDF
        parse_output_path = phase1_parse_pdf(args.input, output_dir, overwrite=args.overwrite)
        print_parse_output_path(str(parse_output_path))
        sys.exit(0)

    elif args.from_parse:
        # Phase 2: Convert from parse result
        model = get_model_name(args)
        try:
            output_md_path = convert_to_markdown(
                args.from_parse, output_dir, model, args.prompt_file
            )
            print_success_message(
                str(output_md_path),
                str(output_dir / "images"),
                str(output_dir / "logs"),
            )
            sys.exit(0)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    else:
        # Both phases: Parse then convert
        # Phase 1
        parse_output_path = phase1_parse_pdf(args.input, output_dir, overwrite=args.overwrite)
        print_parse_output_path(str(parse_output_path))

        # Phase 2 (not yet implemented)
        print(
            "Phase 2 conversion is not yet implemented. "
            f"Use --from-parse {parse_output_path} when Phase 2 is ready.",
            file=sys.stderr,
        )
        sys.exit(0)
