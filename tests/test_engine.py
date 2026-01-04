"""Tests for conversion engine (Phase 1 integration)."""

import tempfile
from pathlib import Path

import pytest

from poc_pdf_to_md.engine import phase1_parse_pdf


class TestPhase1ParsePDF:
    """Test Phase 1 PDF parsing integration."""

    test_pdf: Path
    temp_dir: Path

    def setup_method(self):
        """Setup test environment."""
        self.test_pdf = Path(__file__).parent.parent / "test_data" / "test_data.pdf"
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self):
        """Cleanup test environment."""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_phase1_parse_pdf_success(self):
        """Test successful Phase 1 parsing."""
        parse_output_path = phase1_parse_pdf(str(self.test_pdf), self.temp_dir)
        assert parse_output_path.exists()
        assert parse_output_path.suffix == ".json"

    def test_phase1_parse_pdf_creates_directories(self):
        """Test that required directories are created."""
        phase1_parse_pdf(str(self.test_pdf), self.temp_dir)
        assert (self.temp_dir / "parsed").exists()
        assert (self.temp_dir / "images").exists()

    def test_phase1_parse_pdf_generates_json(self):
        """Test that JSON file is generated."""
        parse_output_path = phase1_parse_pdf(str(self.test_pdf), self.temp_dir)
        import json
        parse_result = json.loads(parse_output_path.read_text())
        assert "schema_version" in parse_result
        assert "created_at" in parse_result
        assert "source_pdf" in parse_result
        assert "total_pages" in parse_result
        assert "blocks" in parse_result

    def test_phase1_parse_pdf_extracts_images(self):
        """Test that images are extracted."""
        phase1_parse_pdf(str(self.test_pdf), self.temp_dir)
        # Check page images
        page_image_files = list((self.temp_dir / "images").glob("page_*.png"))
        assert len(page_image_files) > 0
        
        # Check embedded images
        embedded_image_files = list((self.temp_dir / "images").glob("*.png"))
        embedded_image_files = [f for f in embedded_image_files if not f.name.startswith("page_")]
        embedded_image_files.extend((self.temp_dir / "images").glob("*.jpg"))
        assert len(embedded_image_files) > 0

    def test_phase1_parse_pdf_image_paths_in_json(self):
        """Test that image paths are recorded in JSON."""
        parse_output_path = phase1_parse_pdf(str(self.test_pdf), self.temp_dir)
        import json
        parse_result = json.loads(parse_output_path.read_text())
        
        # Check page images
        page_images = [b for b in parse_result["blocks"] if b.get("type") == "page_image"]
        assert len(page_images) > 0
        for block in page_images[:5]:  # Check first 5 page images
            assert "imagePath" in block
            assert "ext" in block
            assert "width" in block
            assert "height" in block
            assert "page_index" in block
            # Check filename format
            image_path = block["imagePath"]
            assert image_path.startswith("images/page_")
            assert image_path.endswith(".png")
        
        # Check embedded images
        embedded_images = [b for b in parse_result["blocks"] if b.get("type") == "image"]
        for block in embedded_images[:10]:  # Check first 10 embedded image blocks
            assert "imagePath" in block
            assert "ext" in block
            assert "width" in block
            assert "height" in block

    def test_phase1_parse_pdf_block_index_order(self):
        """Test that blockIndex order is correct."""
        parse_output_path = phase1_parse_pdf(str(self.test_pdf), self.temp_dir)
        import json
        parse_result = json.loads(parse_output_path.read_text())
        block_indices = [b.get("blockIndex") for b in parse_result["blocks"]]
        assert block_indices == list(range(len(block_indices)))

    def test_phase1_parse_pdf_timestamp_filename(self):
        """Test that filename uses timestamp format."""
        parse_output_path = phase1_parse_pdf(str(self.test_pdf), self.temp_dir)
        filename = parse_output_path.name
        assert filename.startswith("parse_result_")
        assert filename.endswith(".json")
        timestamp = filename.replace("parse_result_", "").replace(".json", "")
        assert len(timestamp) == 15  # YYYYMMDD_HHMMSS
        assert "_" in timestamp

    def test_phase1_parse_pdf_nonexistent_file(self):
        """Test error when PDF file does not exist."""
        with pytest.raises(RuntimeError):
            phase1_parse_pdf("nonexistent.pdf", self.temp_dir)
