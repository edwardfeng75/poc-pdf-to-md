"""Parse result JSON structure and file operations."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List


def create_parse_result(
    source_pdf: str, total_pages: int, blocks: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Create parse result structure with run-level and block-level metadata."""
    return {
        "schema_version": "1.0",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_pdf": str(source_pdf),
        "total_pages": total_pages,
        "blocks": blocks,
    }


def save_parse_result(
    parse_result: Dict[str, Any], output_dir: Path, overwrite: bool = False
) -> Path:
    """
    Save parse result to JSON file with timestamp.
    
    Args:
        parse_result: Parse result dictionary
        output_dir: Output directory
        overwrite: If True, overwrite existing parse_result.json files
    
    Returns:
        Path to saved file
    """
    parsed_dir = output_dir / "parsed"
    parsed_dir.mkdir(parents=True, exist_ok=True)

    if overwrite:
        # Use fixed filename when overwriting
        filename = "parse_result.json"
        file_path = parsed_dir / filename
    else:
        # Use timestamp to avoid conflicts
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"parse_result_{timestamp}.json"
        file_path = parsed_dir / filename

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(parse_result, f, indent=2, ensure_ascii=False)

    return file_path


def load_parse_result(parse_input_path: Path) -> Dict[str, Any]:
    """Load parse result from JSON file."""
    try:
        with open(parse_input_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(
            f"Failed to load parse result from {parse_input_path}"
        ) from e


def validate_schema_version(parse_result: Dict[str, Any]) -> bool:
    """Validate schema_version compatibility."""
    schema_version = parse_result.get("schema_version", "0.0")
    # For now, only support version 1.0
    return schema_version == "1.0"


def validate_block_index_order(parse_result: Dict[str, Any]) -> bool:
    """Validate blockIndex order is complete and sequential."""
    blocks = parse_result.get("blocks", [])
    if not blocks:
        return True

    block_indices = sorted([block.get("blockIndex") for block in blocks])
    expected_indices = list(range(len(blocks)))

    return block_indices == expected_indices
