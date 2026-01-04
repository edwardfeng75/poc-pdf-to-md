"""Tests for PDF parser."""

from pathlib import Path

import fitz
import pytest

from poc_pdf_to_md.pdf_parser import extract_image, open_pdf, parse_pdf


class TestOpenPDF:
    """Test PDF opening functionality."""

    test_pdf: Path

    def setup_method(self):
        """Setup test environment."""
        self.test_pdf = Path(__file__).parent.parent / "test_data" / "test_data.pdf"

    def teardown_method(self):
        """Cleanup test environment."""
        return

    def test_open_pdf_success(self):
        """Test successfully opening a PDF file."""
        doc = open_pdf(str(self.test_pdf))
        assert doc is not None
        assert isinstance(doc, fitz.Document)
        doc.close()

    def test_open_pdf_nonexistent_file(self):
        """Test error when PDF file does not exist."""
        with pytest.raises(RuntimeError, match="Failed to open PDF file"):
            open_pdf("nonexistent.pdf")


class TestParsePDF:
    """Test PDF parsing functionality."""

    test_pdf: Path
    doc: fitz.Document

    def setup_method(self):
        """Setup test environment."""
        self.test_pdf = Path(__file__).parent.parent / "test_data" / "test_data.pdf"
        self.doc = open_pdf(str(self.test_pdf))

    def teardown_method(self):
        """Cleanup test environment."""
        if self.doc:
            self.doc.close()

    def test_parse_pdf_returns_blocks(self):
        """Test that parse_pdf returns blocks."""
        blocks = parse_pdf(self.doc)
        assert isinstance(blocks, list)
        assert len(blocks) > 0

    def test_parse_pdf_block_structure(self):
        """Test that blocks have correct structure."""
        blocks = parse_pdf(self.doc)
        for block in blocks[:10]:  # Check first 10 blocks
            assert "blockIndex" in block
            assert "page_index" in block
            assert "bbox" in block
            assert "type" in block
            assert block["type"] == "image"  # All blocks are embedded images
            assert "xref" in block  # Embedded images have xref

    def test_parse_pdf_block_index_order(self):
        """Test that blockIndex is sequential."""
        blocks = parse_pdf(self.doc)
        block_indices = [block["blockIndex"] for block in blocks]
        assert block_indices == list(range(len(blocks)))

    def test_parse_pdf_sorting_by_page_index(self):
        """Test that blocks are sorted by page_index."""
        blocks = parse_pdf(self.doc)
        page_indices = [block["page_index"] for block in blocks]
        # Check that page indices are non-decreasing
        for i in range(1, len(page_indices)):
            assert page_indices[i] >= page_indices[i - 1]

    def test_parse_pdf_sorting_by_bbox(self):
        """Test that blocks on same page are sorted by bbox."""
        blocks = parse_pdf(self.doc)
        # Group blocks by page_index
        pages = {}
        for block in blocks:
            page_idx = block["page_index"]
            if page_idx not in pages:
                pages[page_idx] = []
            pages[page_idx].append(block)

        # Check sorting within each page
        for page_idx, page_blocks in list(pages.items())[:5]:  # Check first 5 pages
            if len(page_blocks) > 1:
                for i in range(1, len(page_blocks)):
                    prev_block = page_blocks[i - 1]
                    curr_block = page_blocks[i]
                    prev_y = prev_block["bbox"][1] if len(prev_block["bbox"]) > 1 else 0
                    curr_y = curr_block["bbox"][1] if len(curr_block["bbox"]) > 1 else 0
                    # Y coordinates should be non-decreasing (tolerance applied)
                    assert curr_y >= prev_y - 5  # Allow tolerance


class TestExtractImage:
    """Test image extraction functionality."""

    test_pdf: Path
    doc: fitz.Document

    def setup_method(self):
        """Setup test environment."""
        self.test_pdf = Path(__file__).parent.parent / "test_data" / "test_data.pdf"
        self.doc = open_pdf(str(self.test_pdf))

    def teardown_method(self):
        """Cleanup test environment."""
        if self.doc:
            self.doc.close()

    def test_extract_image_success(self):
        """Test successfully extracting an image."""
        # Find first embedded image block (not text block)
        blocks = parse_pdf(self.doc)
        embedded_image_blocks = [
            b for b in blocks
            if b.get("type") == "image" and not b.get("is_text_block", False)
        ]
        if embedded_image_blocks:
            xref = embedded_image_blocks[0]["xref"]
            image_bytes, image_meta = extract_image(self.doc, xref)
            assert isinstance(image_bytes, bytes)
            assert len(image_bytes) > 0
            assert "ext" in image_meta
            assert "width" in image_meta
            assert "height" in image_meta
            assert "xref" in image_meta
            assert image_meta["xref"] == xref

    def test_extract_image_invalid_xref(self):
        """Test error when xref is invalid."""
        with pytest.raises(RuntimeError, match="Failed to extract image"):
            extract_image(self.doc, 999999)  # Invalid xref
