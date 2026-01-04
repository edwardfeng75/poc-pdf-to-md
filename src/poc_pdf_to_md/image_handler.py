"""Image handling and storage."""

import uuid
from pathlib import Path
from typing import Dict, Any, Tuple


def generate_image_filename(ext: str) -> str:
    """Generate image filename using UUID."""
    return f"{uuid.uuid4()}.{ext}"


def generate_page_image_filename(page_number: int, ext: str = "png") -> str:
    """Generate page image filename using page number as suffix."""
    return f"page_{page_number:04d}.{ext}"


def save_image(
    image_bytes: bytes, output_dir: Path, filename: str, overwrite: bool = False
) -> Path:
    """
    Save image to file and return path relative to output_dir.
    
    Args:
        image_bytes: Image data as bytes
        output_dir: Output directory
        filename: Filename for the image
        overwrite: Whether to overwrite existing file (default: False)
    
    Returns:
        Path relative to output_dir
    """
    images_dir = output_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    image_path = images_dir / filename
    
    if image_path.exists() and not overwrite:
        # If file exists and overwrite is False, generate new UUID filename
        # This only applies to UUID-based filenames, not page_*.png
        if not filename.startswith("page_"):
            import uuid
            ext = image_path.suffix
            filename = f"{uuid.uuid4()}{ext}"
            image_path = images_dir / filename
    
    image_path.write_bytes(image_bytes)
    return image_path.relative_to(output_dir)


def update_parse_result_image_path(
    parse_result: Dict[str, Any], block_index: int, image_path: Path
) -> None:
    """Update imagePath in parse_result for the specified block."""
    for block in parse_result.get("blocks", []):
        if block.get("blockIndex") == block_index:
            if block.get("type") == "image":
                block["imagePath"] = str(image_path)
                break
