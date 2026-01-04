"""Tests for image handling."""

import tempfile
import uuid
from pathlib import Path

import pytest

from poc_pdf_to_md.image_handler import (
    generate_image_filename,
    save_image,
    update_parse_result_image_path,
)


class TestGenerateImageFilename:
    """Test image filename generation."""

    def setup_method(self):
        """Setup test environment."""
        pass

    def teardown_method(self):
        """Cleanup test environment."""
        pass

    def test_generate_image_filename_format(self):
        """Test that generated filename has correct format."""
        filename = generate_image_filename("png")
        assert filename.endswith(".png")
        # Extract UUID part
        uuid_part = filename.replace(".png", "")
        # Verify it's a valid UUID format
        uuid.UUID(uuid_part)

    def test_generate_image_filename_unique(self):
        """Test that generated filenames are unique."""
        filenames = [generate_image_filename("png") for _ in range(10)]
        assert len(filenames) == len(set(filenames))

    def test_generate_image_filename_different_extensions(self):
        """Test filename generation with different extensions."""
        png_filename = generate_image_filename("png")
        jpg_filename = generate_image_filename("jpg")
        assert png_filename.endswith(".png")
        assert jpg_filename.endswith(".jpg")


class TestSaveImage:
    """Test image saving functionality."""

    def setup_method(self):
        """Setup test environment."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_image_bytes = b"fake image data"

    def teardown_method(self):
        """Cleanup test environment."""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_save_image_creates_directory(self):
        """Test that images directory is created."""
        filename = generate_image_filename("png")
        image_path = save_image(self.test_image_bytes, self.temp_dir, filename)
        assert (self.temp_dir / "images").exists()
        assert isinstance(image_path, Path)

    def test_save_image_writes_file(self):
        """Test that image file is written correctly."""
        filename = generate_image_filename("png")
        image_path = save_image(self.test_image_bytes, self.temp_dir, filename)
        full_path = self.temp_dir / image_path
        assert full_path.exists()
        assert full_path.read_bytes() == self.test_image_bytes

    def test_save_image_returns_relative_path(self):
        """Test that returned path is relative to output_dir."""
        filename = generate_image_filename("png")
        image_path = save_image(self.test_image_bytes, self.temp_dir, filename)
        assert not image_path.is_absolute()
        assert str(image_path).startswith("images/")


class TestUpdateParseResultImagePath:
    """Test parse result image path update."""

    def setup_method(self):
        """Setup test environment."""
        self.parse_result = {
            "blocks": [
                {"blockIndex": 0, "type": "text", "text": "test"},
                {"blockIndex": 1, "type": "image", "xref": 123},
                {"blockIndex": 2, "type": "text", "text": "test2"},
            ]
        }

    def teardown_method(self):
        """Cleanup test environment."""
        pass

    def test_update_parse_result_image_path_success(self):
        """Test successfully updating image path."""
        image_path = Path("images/test.png")
        update_parse_result_image_path(self.parse_result, 1, image_path)
        assert self.parse_result["blocks"][1]["imagePath"] == "images/test.png"

    def test_update_parse_result_image_path_text_block(self):
        """Test that text blocks are not updated."""
        original_text = self.parse_result["blocks"][0].copy()
        image_path = Path("images/test.png")
        update_parse_result_image_path(self.parse_result, 0, image_path)
        assert "imagePath" not in self.parse_result["blocks"][0]
        assert self.parse_result["blocks"][0] == original_text

    def test_update_parse_result_image_path_nonexistent_block(self):
        """Test updating non-existent block index."""
        image_path = Path("images/test.png")
        # Should not raise error, just do nothing
        update_parse_result_image_path(self.parse_result, 999, image_path)
