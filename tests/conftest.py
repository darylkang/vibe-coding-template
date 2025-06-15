"""
Shared test fixtures and configuration for pytest.

This module provides common fixtures and configuration that can be used
across all test files in the test suite.
"""

from __future__ import annotations

import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest

from my_package.settings import Settings


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def test_settings(temp_dir: Path) -> Settings:
    """Provide test settings with temporary directories."""
    return Settings(
        debug=True,
        log_level="DEBUG",
        data_dir=temp_dir / "data",
        output_dir=temp_dir / "output",
        enable_rich_output=False,  # Disable for cleaner test output
        enable_metrics=False,
    )


@pytest.fixture
def sample_text_file(temp_dir: Path) -> Path:
    """Create a sample text file for testing."""
    file_path = temp_dir / "sample.txt"
    file_path.write_text("hello\nworld\ntest\n", encoding="utf-8")
    return file_path


@pytest.fixture
def empty_file(temp_dir: Path) -> Path:
    """Create an empty file for testing."""
    file_path = temp_dir / "empty.txt"
    file_path.write_text("", encoding="utf-8")
    return file_path
