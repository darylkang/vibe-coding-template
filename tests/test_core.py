"""
Test suite for the core module.

This file demonstrates basic testing patterns for modern Python applications.
"""

from __future__ import annotations

import pytest

from my_package import __version__
from my_package.core import MyPackage, ProcessingRequest, ProcessingResult
from my_package.settings import Settings


class TestProcessingRequest:
    """Test cases for ProcessingRequest model."""

    def test_processing_request_creation(self) -> None:
        """Test creating a ProcessingRequest with valid data."""
        request = ProcessingRequest(input_data="hello", transform_type="uppercase")
        assert request.input_data == "hello"
        assert request.transform_type == "uppercase"

    def test_processing_request_defaults(self) -> None:
        """Test ProcessingRequest default values."""
        request = ProcessingRequest(input_data="test")
        assert request.transform_type == "uppercase"


class TestProcessingResult:
    """Test cases for ProcessingResult model."""

    def test_processing_result_creation(self) -> None:
        """Test creating a ProcessingResult with valid data."""
        result = ProcessingResult(output_data="HELLO")
        assert result.output_data == "HELLO"
        assert result.success is True
        assert result.metadata == {}

    def test_processing_result_with_metadata(self) -> None:
        """Test creating a ProcessingResult with metadata."""
        metadata = {"input_length": 5, "output_length": 5}
        result = ProcessingResult(output_data="HELLO", metadata=metadata)
        assert result.metadata == metadata


class TestMyPackage:
    """Test cases for MyPackage class."""

    @pytest.fixture
    def package(self) -> MyPackage:
        """Provide MyPackage instance for testing."""
        settings = Settings(debug=True)
        return MyPackage(settings=settings)

    def test_package_initialization(self, package: MyPackage) -> None:
        """Test MyPackage initialization."""
        assert package.settings is not None

    @pytest.mark.parametrize(
        "input_text,transform_type,expected_output",
        [
            ("hello", "uppercase", "HELLO"),
            ("HELLO", "lowercase", "hello"),
            ("hello world", "title", "Hello World"),
            ("hello", "reverse", "olleh"),
        ],
    )
    def test_process_transformations(
        self,
        package: MyPackage,
        input_text: str,
        transform_type: str,
        expected_output: str,
    ) -> None:
        """Test various transformation types."""
        result = package.process(input_text, transform_type)
        assert result.success is True
        assert result.output_data == expected_output

    def test_process_invalid_transform(self, package: MyPackage) -> None:
        """Test processing with invalid transformation type."""
        result = package.process("hello", "invalid_transform")
        assert result.success is False
        assert "error" in result.metadata

    def test_get_stats(self, package: MyPackage) -> None:
        """Test get_stats method."""
        stats = package.get_stats()
        assert "version" in stats
        assert "settings" in stats
        assert stats["version"] == __version__
