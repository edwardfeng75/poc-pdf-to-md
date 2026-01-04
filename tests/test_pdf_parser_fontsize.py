"""Tests for PDF parser font size extraction."""

from pathlib import Path

from poc_pdf_to_md.pdf_parser import open_pdf, parse_pdf


class TestFontSizeExtraction:
    """Test font size extraction from PDF."""

    test_pdf: Path
    doc: object

    def setup_method(self):
        """Setup test environment."""
        self.test_pdf = Path(__file__).parent.parent / "test_data" / "test_data.pdf"
        self.doc = open_pdf(str(self.test_pdf))

    def teardown_method(self):
        """Cleanup test environment."""
        if self.doc:
            self.doc.close()

    def test_font_size_extraction(self):
        """Test that font size extraction is no longer used (text blocks removed)."""
        # Note: Text blocks are no longer processed, so font size extraction
        # is not applicable. This test is kept for reference but will always pass
        # since we're not extracting text blocks anymore.
        blocks = parse_pdf(self.doc)
        # All blocks should be embedded images only
        assert all(b.get("type") == "image" for b in blocks)
        assert all("xref" in b for b in blocks)

    def test_font_size_format(self):
        """Test that font size is a valid number."""
        blocks = parse_pdf(self.doc)
        text_blocks = [
            b for b in blocks
            if b.get("is_text_block", False)
        ]
        
        for block in text_blocks[:20]:  # Check first 20 text blocks
            if "fontSize" in block:
                assert isinstance(block["fontSize"], (int, float))
                assert block["fontSize"] > 0

    def test_font_size_min_max(self):
        """Test that font size min/max are present when sizes differ."""
        blocks = parse_pdf(self.doc)
        text_blocks = [
            b for b in blocks
            if b.get("is_text_block", False)
        ]
        
        for block in text_blocks[:50]:  # Check first 50 text blocks
            if "fontSize" in block:
                # If fontSizeMax exists, fontSizeMin should also exist
                if "fontSizeMax" in block:
                    assert "fontSizeMin" in block
                    assert block["fontSizeMax"] >= block["fontSizeMin"]
                    assert block["fontSizeMax"] >= block["fontSize"]

    def test_font_size_average_calculation(self):
        """Test that font size average is calculated correctly."""
        blocks = parse_pdf(self.doc)
        text_blocks = [
            b for b in blocks
            if b.get("is_text_block", False)
        ]
        
        for block in text_blocks[:20]:
            if "fontSize" in block:
                # Average should be between min and max if they exist
                if "fontSizeMin" in block and "fontSizeMax" in block:
                    assert block["fontSizeMin"] <= block["fontSize"] <= block["fontSizeMax"]
