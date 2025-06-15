"""
Test suite for the core module.

This file provides comprehensive test coverage for the MyPackage class
and related functionality. It demonstrates best practices for pytest
including fixtures, parametrized tests, and proper test organization.

INSTRUCTIONS FOR CURSOR:
- Add new test functions for any new features
- Use descriptive test names that explain what is being tested
- Group related tests using classes if needed
- Use fixtures for common setup/teardown operations
- Test both happy path and error conditions
"""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest

from my_package.core import MyPackage, ProcessingRequest, ProcessingResult
from my_package.settings import Settings


class TestProcessingRequest:
    """Test cases for ProcessingRequest model."""

    def test_processing_request_creation(self) -> None:
        """Test creating a ProcessingRequest with valid data."""
        request = ProcessingRequest(input_data="hello", transform_type="uppercase")
        assert request.input_data == "hello"
        assert request.transform_type == "uppercase"
        assert request.options == {}

    def test_processing_request_with_options(self) -> None:
        """Test creating a ProcessingRequest with custom options."""
        options = {"custom": "value"}
        request = ProcessingRequest(
            input_data="hello",
            transform_type="lowercase", 
            options=options
        )
        assert request.options == options

    def test_processing_request_validation(self) -> None:
        """Test that ProcessingRequest validates required fields."""
        with pytest.raises(ValueError):
            ProcessingRequest()  # Missing required input_data


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

    def test_processing_result_failure(self) -> None:
        """Test creating a failed ProcessingResult."""
        result = ProcessingResult(
            output_data="",
            success=False,
            metadata={"error": "Something went wrong"}
        )
        assert result.success is False
        assert "error" in result.metadata


class TestMyPackage:
    """Test cases for MyPackage class."""

    @pytest.fixture
    def settings(self) -> Settings:
        """Provide test settings."""
        return Settings(debug=True, log_level="DEBUG")

    @pytest.fixture
    def package(self, settings: Settings) -> MyPackage:
        """Provide MyPackage instance for testing."""
        return MyPackage(settings=settings, verbose=False)

    @pytest.fixture
    def verbose_package(self, settings: Settings) -> MyPackage:
        """Provide verbose MyPackage instance for testing."""
        return MyPackage(settings=settings, verbose=True)

    def test_package_initialization(self, package: MyPackage) -> None:
        """Test MyPackage initialization."""
        assert package.settings is not None
        assert package.verbose is False

    def test_package_initialization_verbose(self, verbose_package: MyPackage) -> None:
        """Test MyPackage initialization with verbose mode."""
        assert verbose_package.verbose is True

    def test_package_initialization_default_settings(self) -> None:
        """Test MyPackage initialization with default settings."""
        package = MyPackage()
        assert package.settings is not None

    @pytest.mark.parametrize("input_text,transform_type,expected_output", [
        ("hello", "uppercase", "HELLO"),
        ("HELLO", "lowercase", "hello"),
        ("hello world", "title", "Hello World"),
        ("hello world", "capitalize", "Hello world"),
        ("hello", "reverse", "olleh"),
    ])
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
        assert result.metadata["transform_type"] == transform_type
        assert result.metadata["input_length"] == len(input_text)
        assert result.metadata["output_length"] == len(expected_output)

    def test_process_invalid_transform(self, package: MyPackage) -> None:
        """Test processing with invalid transformation type."""
        result = package.process("hello", "invalid_transform")
        
        assert result.success is False
        assert result.output_data == ""
        assert "error" in result.metadata
        assert "Unsupported transform_type" in result.metadata["error"]

    def test_process_empty_input(self, package: MyPackage) -> None:
        """Test processing with empty input."""
        result = package.process("", "uppercase")
        
        assert result.success is True
        assert result.output_data == ""
        assert result.metadata["input_length"] == 0
        assert result.metadata["output_length"] == 0

    def test_process_verbose_logging(self, verbose_package: MyPackage) -> None:
        """Test that verbose mode enables logging."""
        with patch("my_package.core.logger") as mock_logger:
            verbose_package.process("hello", "uppercase")
            
            # Check that info logs were called
            mock_logger.info.assert_called()

    def test_batch_process(self, package: MyPackage) -> None:
        """Test batch processing functionality."""
        inputs = ["hello", "world", "test"]
        results = package.batch_process(inputs, "uppercase")
        
        assert len(results) == 3
        assert all(r.success for r in results)
        
        expected_outputs = ["HELLO", "WORLD", "TEST"]
        actual_outputs = [r.output_data for r in results]
        assert actual_outputs == expected_outputs

    def test_batch_process_empty_list(self, package: MyPackage) -> None:
        """Test batch processing with empty input list."""
        results = package.batch_process([], "uppercase")
        assert results == []

    def test_batch_process_mixed_success(self, package: MyPackage) -> None:
        """Test batch processing with some failures."""
        inputs = ["hello", "world"]
        
        # Mock the process method to fail on second call
        with patch.object(package, 'process') as mock_process:
            mock_process.side_effect = [
                ProcessingResult(output_data="HELLO"),
                ProcessingResult(output_data="", success=False, metadata={"error": "Test error"})
            ]
            
            results = package.batch_process(inputs, "uppercase")
            
            assert len(results) == 2
            assert results[0].success is True
            assert results[1].success is False

    def test_get_stats(self, package: MyPackage) -> None:
        """Test get_stats method."""
        stats = package.get_stats()
        
        assert "version" in stats
        assert "verbose_mode" in stats
        assert "settings" in stats
        assert stats["verbose_mode"] is False

    def test_get_stats_verbose(self, verbose_package: MyPackage) -> None:
        """Test get_stats method with verbose package."""
        stats = verbose_package.get_stats()
        assert stats["verbose_mode"] is True


class TestIntegration:
    """Integration tests for the complete workflow."""

    def test_end_to_end_processing(self) -> None:
        """Test complete processing workflow."""
        settings = Settings(debug=False)
        package = MyPackage(settings=settings, verbose=False)
        
        # Process single item
        result = package.process("hello world", "title")
        assert result.success is True
        assert result.output_data == "Hello World"
        
        # Get stats
        stats = package.get_stats()
        assert stats["version"] == "0.1.0"

    def test_error_handling_workflow(self) -> None:
        """Test error handling in complete workflow."""
        package = MyPackage()
        
        # Test invalid transformation
        result = package.process("test", "nonexistent")
        assert result.success is False
        assert "error" in result.metadata
