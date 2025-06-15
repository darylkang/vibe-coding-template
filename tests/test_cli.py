"""
Test suite for the CLI module.

This file demonstrates basic CLI testing patterns.
"""

from __future__ import annotations

from typer.testing import CliRunner

from my_package import __version__
from my_package.cli import app


class TestCLI:
    """Test cases for CLI commands."""

    def test_cli_help(self) -> None:
        """Test CLI help command."""
        runner = CliRunner()
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert (
            "Modern Python development made easy with TDD enforcement" in result.stdout
        )

    def test_version_command(self) -> None:
        """Test version command."""
        runner = CliRunner()
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert f"vibe version: {__version__}" in result.stdout

    def test_process_command_basic(self) -> None:
        """Test basic process command."""
        runner = CliRunner()
        result = runner.invoke(app, ["process", "hello world"])
        assert result.exit_code == 0
        assert "HELLO WORLD" in result.stdout

    def test_process_command_with_transform(self) -> None:
        """Test process command with transform option."""
        runner = CliRunner()
        result = runner.invoke(app, ["process", "HELLO", "--transform", "lowercase"])
        assert result.exit_code == 0
        assert "hello" in result.stdout

    def test_info_command(self) -> None:
        """Test info command."""
        runner = CliRunner()
        result = runner.invoke(app, ["info"])
        assert result.exit_code == 0
        assert "Package Information" in result.stdout
        assert f"Version: {__version__}" in result.stdout
