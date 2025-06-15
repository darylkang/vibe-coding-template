"""
Test suite for the CLI module.

This file provides comprehensive test coverage for the Typer CLI
including command testing and output verification.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from my_package.cli import app


class TestCLI:
    """Test cases for CLI commands."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Provide CLI test runner."""
        return CliRunner()

    def test_cli_help(self, runner: CliRunner) -> None:
        """Test CLI help command."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "Vibe Coding Template" in result.stdout

    def test_version_command(self, runner: CliRunner) -> None:
        """Test version command."""
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "vibe version: 0.1.0" in result.stdout

    def test_run_command_basic(self, runner: CliRunner) -> None:
        """Test basic run command."""
        result = runner.invoke(app, ["run", "hello world"])
        assert result.exit_code == 0
        assert "HELLO WORLD" in result.stdout

    def test_run_command_with_transform(self, runner: CliRunner) -> None:
        """Test run command with different transforms."""
        # Test lowercase
        result = runner.invoke(app, ["run", "HELLO WORLD", "--transform", "lowercase"])
        assert result.exit_code == 0
        assert "hello world" in result.stdout

        # Test title
        result = runner.invoke(app, ["run", "hello world", "--transform", "title"])
        assert result.exit_code == 0
        assert "Hello World" in result.stdout

    def test_run_command_verbose(self, runner: CliRunner) -> None:
        """Test run command with verbose output."""
        result = runner.invoke(app, ["run", "hello", "--verbose"])
        assert result.exit_code == 0
        assert "HELLO" in result.stdout

    def test_run_command_with_output_file(self, runner: CliRunner) -> None:
        """Test run command with output file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_file = Path(tmp_dir) / "output.txt"
            result = runner.invoke(
                app, ["run", "hello world", "--output", str(output_file)]
            )
            assert result.exit_code == 0
            assert output_file.exists()
            assert output_file.read_text() == "HELLO WORLD"

    def test_run_command_invalid_transform(self, runner: CliRunner) -> None:
        """Test run command with invalid transform."""
        result = runner.invoke(app, ["run", "hello", "--transform", "invalid"])
        assert result.exit_code == 1
        assert "Processing failed" in result.stdout

    def test_batch_command(self, runner: CliRunner) -> None:
        """Test batch command with file input."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_file = Path(tmp_dir) / "input.txt"
            input_file.write_text("hello\nworld\ntest\n")

            result = runner.invoke(app, ["batch", str(input_file)])
            assert result.exit_code == 0
            assert "Processed 3/3 items successfully" in result.stdout

    def test_batch_command_with_output(self, runner: CliRunner) -> None:
        """Test batch command with output file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_file = Path(tmp_dir) / "input.txt"
            output_file = Path(tmp_dir) / "output.txt"
            input_file.write_text("hello\nworld\n")

            result = runner.invoke(
                app, ["batch", str(input_file), "--output", str(output_file)]
            )
            assert result.exit_code == 0
            assert output_file.exists()

            output_content = output_file.read_text()
            assert "HELLO" in output_content
            assert "WORLD" in output_content

    def test_batch_command_with_transform(self, runner: CliRunner) -> None:
        """Test batch command with different transform."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_file = Path(tmp_dir) / "input.txt"
            input_file.write_text("hello world\ntest case\n")

            result = runner.invoke(
                app, ["batch", str(input_file), "--transform", "title"]
            )
            assert result.exit_code == 0
            assert "Processed 2/2 items successfully" in result.stdout

    def test_batch_command_nonexistent_file(self, runner: CliRunner) -> None:
        """Test batch command with nonexistent input file."""
        result = runner.invoke(app, ["batch", "nonexistent.txt"])
        assert result.exit_code == 1
        assert "Input file not found" in result.stdout

    def test_batch_command_empty_file(self, runner: CliRunner) -> None:
        """Test batch command with empty input file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_file = Path(tmp_dir) / "empty.txt"
            input_file.write_text("")

            result = runner.invoke(app, ["batch", str(input_file)])
            assert result.exit_code == 1
            assert "No valid lines found" in result.stdout

    def test_batch_command_verbose(self, runner: CliRunner) -> None:
        """Test batch command with verbose output."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_file = Path(tmp_dir) / "input.txt"
            input_file.write_text("hello\nworld\n")

            result = runner.invoke(app, ["batch", str(input_file), "--verbose"])
            assert result.exit_code == 0
            assert "Batch Summary" in result.stdout

    def test_info_command(self, runner: CliRunner) -> None:
        """Test info command."""
        result = runner.invoke(app, ["info"])
        assert result.exit_code == 0
        assert "Package Information" in result.stdout
        assert "Version" in result.stdout
        assert "0.1.0" in result.stdout

    def test_transforms_command(self, runner: CliRunner) -> None:
        """Test transforms command."""
        result = runner.invoke(app, ["transforms"])
        assert result.exit_code == 0
        assert "Available Transformations" in result.stdout
        assert "uppercase" in result.stdout
        assert "lowercase" in result.stdout
        assert "title" in result.stdout
        assert "reverse" in result.stdout
        assert "capitalize" in result.stdout

    def test_cli_error_handling(self, runner: CliRunner) -> None:
        """Test CLI error handling."""
        # Test with exception in processing
        with patch("my_package.cli.MyPackage") as mock_package:
            mock_package.side_effect = Exception("Test error")
            result = runner.invoke(app, ["run", "hello"])
            assert result.exit_code == 1
            assert "Error: Test error" in result.stdout

    def test_helper_functions(self) -> None:
        """Test CLI helper functions."""
        from my_package.cli import _get_transform_example

        assert _get_transform_example("uppercase") == "hello → HELLO"
        assert _get_transform_example("lowercase") == "HELLO → hello"
        assert _get_transform_example("unknown") == "hello → ?"
