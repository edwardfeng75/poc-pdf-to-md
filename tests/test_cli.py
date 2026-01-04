"""Tests for CLI interface."""

import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from poc_pdf_to_md.cli import (
    parse_args,
    get_model_name,
    print_parse_output_path,
    print_success_message,
)


class TestCLIParseArgs:
    """Test CLI argument parsing."""

    def setup_method(self):
        """Setup test environment."""
        self.test_pdf = Path(__file__).parent.parent / "test_data" / "test_data.pdf"
        self.temp_dir = tempfile.mkdtemp()
        self.temp_pdf = Path(self.temp_dir) / "test.pdf"

    def teardown_method(self):
        """Cleanup test environment."""
        import shutil
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_parse_args_with_valid_input(self):
        """Test parsing valid input arguments."""
        test_args = [
            "--input",
            str(self.test_pdf),
            "--output",
            self.temp_dir,
        ]
        with patch.object(sys, "argv", ["test_cli.py"] + test_args):
            args = parse_args()
            assert args.input == str(self.test_pdf)
            assert args.output == self.temp_dir
            assert args.parse_only is False
            assert args.from_parse is None
            assert args.prompt_file == "prompts/phase2_page_to_md.md"

    def test_parse_args_with_parse_only(self):
        """Test parsing --parse-only flag."""
        test_args = [
            "--input",
            str(self.test_pdf),
            "--parse-only",
        ]
        with patch.object(sys, "argv", ["test_cli.py"] + test_args):
            args = parse_args()
            assert args.parse_only is True
            assert args.from_parse is None
            assert args.prompt_file == "prompts/phase2_page_to_md.md"

    def test_parse_args_with_from_parse(self):
        """Test parsing --from-parse argument."""
        parse_file = Path(self.temp_dir) / "parse_result.json"
        parse_file.write_text('{"schema_version": "1.0"}')
        test_args = [
            "--from-parse",
            str(parse_file),
        ]
        with patch.object(sys, "argv", ["test_cli.py"] + test_args):
            args = parse_args()
            assert args.from_parse == str(parse_file)
            assert args.parse_only is False
            assert args.prompt_file == "prompts/phase2_page_to_md.md"

    def test_parse_args_mutual_exclusivity_error(self):
        """Test that --parse-only and --from-parse cannot be used together."""
        parse_file = Path(self.temp_dir) / "parse_result.json"
        parse_file.write_text('{"schema_version": "1.0"}')
        test_args = [
            "--input",
            str(self.test_pdf),
            "--parse-only",
            "--from-parse",
            str(parse_file),
        ]
        with patch.object(sys, "argv", ["test_cli.py"] + test_args):
            with patch("sys.exit") as mock_exit:
                parse_args()
                mock_exit.assert_called_once_with(1)

    def test_parse_args_nonexistent_pdf_error(self):
        """Test error when PDF file does not exist."""
        test_args = [
            "--input",
            "nonexistent.pdf",
        ]
        with patch.object(sys, "argv", ["test_cli.py"] + test_args):
            with patch("sys.exit") as mock_exit:
                parse_args()
                # May be called multiple times due to multiple validation checks
                assert mock_exit.called
                assert mock_exit.call_args[0][0] == 1

    def test_parse_args_nonexistent_parse_file_error(self):
        """Test error when parse result file does not exist."""
        test_args = [
            "--from-parse",
            "nonexistent.json",
        ]
        with patch.object(sys, "argv", ["test_cli.py"] + test_args):
            with patch("sys.exit") as mock_exit:
                parse_args()
                # May be called multiple times due to multiple validation checks
                assert mock_exit.called
                assert mock_exit.call_args[0][0] == 1


class TestGetModelName:
    """Test model name resolution."""

    def setup_method(self):
        """Setup test environment."""
        self.original_env = os.environ.get("GEMINI_MODEL")

    def teardown_method(self):
        """Cleanup test environment."""
        if self.original_env:
            os.environ["GEMINI_MODEL"] = self.original_env
        elif "GEMINI_MODEL" in os.environ:
            del os.environ["GEMINI_MODEL"]

    def test_get_model_name_from_cli_arg(self):
        """Test model name from CLI argument."""
        from argparse import Namespace
        args = Namespace(model="test-model")
        assert get_model_name(args) == "test-model"

    def test_get_model_name_from_env(self):
        """Test model name from environment variable."""
        os.environ["GEMINI_MODEL"] = "env-model"
        from argparse import Namespace
        args = Namespace(model=None)
        assert get_model_name(args) == "env-model"

    def test_get_model_name_default(self):
        """Test default model name."""
        if "GEMINI_MODEL" in os.environ:
            del os.environ["GEMINI_MODEL"]
        from argparse import Namespace
        args = Namespace(model=None)
        assert get_model_name(args) == "gemini-3-pro-preview"


class TestPrintFunctions:
    """Test print functions."""

    def setup_method(self):
        """Setup test environment."""
        pass

    def teardown_method(self):
        """Cleanup test environment."""
        pass

    def test_print_parse_output_path(self, capsys):
        """Test print_parse_output_path function."""
        print_parse_output_path("test/path.json")
        captured = capsys.readouterr()
        assert "Parse output saved to: test/path.json" in captured.out
        assert "Please review the parsing results" in captured.out

    def test_print_success_message(self, capsys):
        """Test print_success_message function."""
        print_success_message("output.md", "images/", "logs/")
        captured = capsys.readouterr()
        assert "Conversion completed successfully!" in captured.out
        assert "output.md" in captured.out
        assert "images/" in captured.out
        assert "logs/" in captured.out
