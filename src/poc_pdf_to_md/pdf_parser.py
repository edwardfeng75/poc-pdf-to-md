"""PDF parser using PyMuPDF."""

import fitz  # PyMuPDF
from typing import Any, Callable, Dict, List, Optional, Tuple


def open_pdf(pdf_path: str) -> fitz.Document:
    """Open PDF file and return document object."""
    try:
        doc = fitz.open(pdf_path)
        return doc
    except Exception as e:
        raise RuntimeError(f"Failed to open PDF file: {pdf_path}") from e


def extract_image(doc: fitz.Document, xref: int) -> Tuple[bytes, Dict[str, Any]]:
    """Extract image from PDF by xref."""
    try:
        image_data = doc.extract_image(xref)
        image_bytes = image_data["image"]
        image_meta = {
            "ext": image_data["ext"],
            "width": image_data["width"],
            "height": image_data["height"],
            "xref": xref,
        }
        return image_bytes, image_meta
    except Exception as e:
        raise RuntimeError(f"Failed to extract image with xref {xref}") from e


def render_page_as_image(
    page: fitz.Page, zoom: float = 2.0
) -> Tuple[bytes, Dict[str, Any]]:
    """
    Render entire PDF page as image.
    
    Args:
        page: PDF page object
        zoom: Zoom factor for rendering (default: 2.0 for better quality)
    
    Returns:
        Tuple of (image_bytes, image_meta)
    """
    try:
        # Render the entire page as pixmap
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PNG bytes
        image_bytes = pix.tobytes("png")
        
        # Get page dimensions
        width = pix.width
        height = pix.height
        
        image_meta = {
            "ext": "png",
            "width": width,
            "height": height,
            "zoom": zoom,
        }
        
        return image_bytes, image_meta
    except Exception as e:
        raise RuntimeError("Failed to render page as image") from e


def parse_pdf(
    doc: fitz.Document,
    *,
    progress_cb: Optional[Callable[[int, int], None]] = None,
) -> List[Dict[str, Any]]:
    """
    Parse PDF and return embedded image blocks only.
    
    Text blocks are not processed - only embedded images are extracted.
    """
    blocks: List[Dict[str, Any]] = []
    total_pages = len(doc)

    for page_index, page in enumerate(doc):
        if progress_cb is not None:
            progress_cb(page_index + 1, total_pages)

        # Extract embedded images only (no text blocks)
        image_list = page.get_images(full=True)
        for img in image_list:
            xref = img[0]
            bbox_list = page.get_image_bbox(img)
            bbox = [bbox_list.x0, bbox_list.y0, bbox_list.x1, bbox_list.y1]
            blocks.append(
                {
                    "page_index": page_index,
                    "bbox": bbox,
                    "type": "image",
                    "xref": xref,
                }
            )

    # Sort blocks: page_index -> bbox.y -> bbox.x
    def sort_key(block: Dict[str, Any]) -> Tuple[int, float, float]:
        page_idx = block["page_index"]
        bbox = block["bbox"]
        y = bbox[1] if len(bbox) > 1 else 0.0
        x = bbox[0] if len(bbox) > 0 else 0.0
        return (page_idx, y, x)

    blocks.sort(key=sort_key)

    # Add blockIndex
    for index, block in enumerate(blocks):
        block["blockIndex"] = index

    return blocks
