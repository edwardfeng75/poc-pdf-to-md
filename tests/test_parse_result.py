"""Tests for parse result operations."""

import json
import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from poc_pdf_to_md.parse_result import (
    create_parse_result,
    load_parse_result,
    save_parse_result,
    validate_block_index_order,
    validate_schema_version,
)


class TestCreateParseResult:
    """Test parse result creation."""

    def setup_method(self):
        """Setup test environment."""
        self.test_blocks = [
            {"blockIndex": 0, "page_index": 0, "type": "text", "text": "test"},
            {"blockIndex": 1, "page_index": 0, "type": "image", "xref": 123},
        ]

    def teardown_method(self):
        """Cleanup test environment."""
        pass

    def test_create_parse_result_structure(self):
        """Test that parse result has correct structure."""
        result = create_parse_result("test.pdf", 10, self.test_blocks)
        assert "schema_version" in result
        assert "created_at" in result
        assert "source_pdf" in result
        assert "total_pages" in result
        assert "blocks" in result

    def test_create_parse_result_values(self):
        """Test that parse result has correct values."""
        result = create_parse_result("test.pdf", 10, self.test_blocks)
        assert result["schema_version"] == "1.0"
        assert result["source_pdf"] == "test.pdf"
        assert result["total_pages"] == 10
        assert result["blocks"] == self.test_blocks

    def test_create_parse_result_created_at_format(self):
        """Test that created_at is in ISO 8601 format."""
        result = create_parse_result("test.pdf", 10, self.test_blocks)
        created_at = result["created_at"]
        # Should end with Z and be parseable
        assert created_at.endswith("Z")
        datetime.fromisoformat(created_at.replace("Z", "+00:00"))


class TestSaveParseResult:
    """Test parse result saving."""

    def setup_method(self):
        """Setup test environment."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.parse_result = {
            "schema_version": "1.0",
            "created_at": "2025-01-01T00:00:00Z",
            "source_pdf": "test.pdf",
            "total_pages": 10,
            "blocks": [],
        }

    def teardown_method(self):
        """Cleanup test environment."""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_save_parse_result_creates_directory(self):
        """Test that parsed directory is created."""
        file_path = save_parse_result(self.parse_result, self.temp_dir)
        assert (self.temp_dir / "parsed").exists()
        assert file_path.exists()

    def test_save_parse_result_filename_format(self):
        """Test that filename has correct timestamp format."""
        file_path = save_parse_result(self.parse_result, self.temp_dir)
        filename = file_path.name
        assert filename.startswith("parse_result_")
        assert filename.endswith(".json")
        # Extract timestamp
        timestamp = filename.replace("parse_result_", "").replace(".json", "")
        # Should be YYYYMMDD_HHMMSS format
        assert len(timestamp) == 15
        assert "_" in timestamp

    def test_save_parse_result_content(self):
        """Test that saved content is correct."""
        file_path = save_parse_result(self.parse_result, self.temp_dir)
        loaded = json.loads(file_path.read_text())
        assert loaded == self.parse_result


class TestLoadParseResult:
    """Test parse result loading."""

    def setup_method(self):
        """Setup test environment."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.parse_result = {
            "schema_version": "1.0",
            "created_at": "2025-01-01T00:00:00Z",
            "source_pdf": "test.pdf",
            "total_pages": 10,
            "blocks": [],
        }
        self.test_file = self.temp_dir / "test.json"
        self.test_file.write_text(json.dumps(self.parse_result, indent=2))

    def teardown_method(self):
        """Cleanup test environment."""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_load_parse_result_success(self):
        """Test successfully loading parse result."""
        loaded = load_parse_result(self.test_file)
        assert loaded == self.parse_result

    def test_load_parse_result_nonexistent_file(self):
        """Test error when file does not exist."""
        with pytest.raises(RuntimeError, match="Failed to load parse result"):
            load_parse_result(Path("nonexistent.json"))

    def test_load_parse_result_invalid_json(self):
        """Test error when JSON is invalid."""
        invalid_file = self.temp_dir / "invalid.json"
        invalid_file.write_text("invalid json")
        with pytest.raises(RuntimeError):
            load_parse_result(invalid_file)


class TestValidateSchemaVersion:
    """Test schema version validation."""

    def setup_method(self):
        """Setup test environment."""
        pass

    def teardown_method(self):
        """Cleanup test environment."""
        pass

    def test_validate_schema_version_valid(self):
        """Test validation with valid schema version."""
        parse_result = {"schema_version": "1.0"}
        assert validate_schema_version(parse_result) is True

    def test_validate_schema_version_invalid(self):
        """Test validation with invalid schema version."""
        parse_result = {"schema_version": "2.0"}
        assert validate_schema_version(parse_result) is False

    def test_validate_schema_version_missing(self):
        """Test validation with missing schema version."""
        parse_result = {}
        assert validate_schema_version(parse_result) is False


class TestValidateBlockIndexOrder:
    """Test block index order validation."""

    def setup_method(self):
        """Setup test environment."""
        pass

    def teardown_method(self):
        """Cleanup test environment."""
        pass

    def test_validate_block_index_order_valid(self):
        """Test validation with valid block index order."""
        parse_result = {
            "blocks": [
                {"blockIndex": 0},
                {"blockIndex": 1},
                {"blockIndex": 2},
            ]
        }
        assert validate_block_index_order(parse_result) is True

    def test_validate_block_index_order_invalid(self):
        """Test validation with invalid block index order."""
        parse_result = {
            "blocks": [
                {"blockIndex": 0},
                {"blockIndex": 2},  # Missing 1
                {"blockIndex": 3},
            ]
        }
        assert validate_block_index_order(parse_result) is False

    def test_validate_block_index_order_empty(self):
        """Test validation with empty blocks."""
        parse_result = {"blocks": []}
        assert validate_block_index_order(parse_result) is True

    def test_validate_block_index_order_missing_blocks(self):
        """Test validation with missing blocks key."""
        parse_result = {}
        assert validate_block_index_order(parse_result) is True
