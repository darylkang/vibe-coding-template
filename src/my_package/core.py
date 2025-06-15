"""
Core logic for the application.

This module contains the main business logic and data processing functions.
It demonstrates best practices for structuring a modern Python application
with proper type hints, Pydantic models, and clear separation of concerns.

INSTRUCTIONS FOR CURSOR:
- Implement functions based on top-level docstrings or inline comments
- Use Pydantic models for structured inputs/outputs
- Keep each function focused, testable, and well-documented
- Add new methods to MyPackage class as needed
- Consider breaking into separate modules as the project grows
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, Field
from rich.console import Console
from rich.logging import RichHandler

from my_package.settings import Settings

# Configure logging with Rich
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger(__name__)
console = Console()


class ProcessingRequest(BaseModel):
    """Request model for processing operations."""

    input_data: str = Field(..., description="Input data to be processed")
    transform_type: str = Field(
        default="uppercase",
        description="Type of transformation to apply",
    )
    options: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional options for processing",
    )


class ProcessingResult(BaseModel):
    """Result model for processing operations."""

    output_data: str = Field(..., description="Processed output data")
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata about the processing operation",
    )
    success: bool = Field(default=True, description="Whether processing succeeded")


class MyPackage:
    """
    Main interface class for the package.

    This class serves as the central point of interaction for the package,
    providing a clean API for common operations while maintaining state
    and configuration.

    INSTRUCTIONS FOR CURSOR:
    - Add methods that wrap or coordinate internal modules
    - Ensure methods are well-documented with clear parameters and return types
    - Use Pydantic models for complex inputs/outputs
    - Keep methods focused on single responsibilities

    Example:
        >>> package = MyPackage(verbose=True)
        >>> result = package.process("hello world")
        >>> print(result.output_data)
        HELLO WORLD
    """

    def __init__(self, settings: Settings | None = None, verbose: bool = False) -> None:
        """
        Initialize the main package interface.

        Args:
            settings: Application settings. If None, will load from environment.
            verbose: If True, enables verbose output/logging.
        """
        self.settings = settings or Settings()
        self.verbose = verbose
        
        if self.verbose:
            logger.setLevel(logging.DEBUG)
            logger.debug("MyPackage initialized with verbose mode enabled")

    def process(self, input_data: str, transform_type: str = "uppercase") -> ProcessingResult:
        """
        Process input data with the specified transformation.

        Args:
            input_data: Raw input data to be processed.
            transform_type: Type of transformation to apply.

        Returns:
            ProcessingResult containing the processed data and metadata.

        Raises:
            ValueError: If transform_type is not supported.
        """
        if self.verbose:
            logger.info(f"Processing input with transform: {transform_type}")

        request = ProcessingRequest(
            input_data=input_data,
            transform_type=transform_type,
        )
        
        try:
            result = self._apply_transformation(request)
            
            if self.verbose:
                logger.info(f"Processing completed successfully: {result.output_data}")
            
            return result
            
        except Exception as e:
            logger.error(f"Processing failed: {e}")
            return ProcessingResult(
                output_data="",
                success=False,
                metadata={"error": str(e)},
            )

    def _apply_transformation(self, request: ProcessingRequest) -> ProcessingResult:
        """
        Apply the requested transformation to the input data.
        
        This is a private method that handles the actual transformation logic.
        
        Args:
            request: The processing request containing input and parameters.
            
        Returns:
            ProcessingResult with the transformed data.
            
        Raises:
            ValueError: If the transformation type is not supported.
        """
        transformations = {
            "uppercase": lambda x: x.upper(),
            "lowercase": lambda x: x.lower(),
            "title": lambda x: x.title(),
            "reverse": lambda x: x[::-1],
            "capitalize": lambda x: x.capitalize(),
        }
        
        if request.transform_type not in transformations:
            supported = ", ".join(transformations.keys())
            raise ValueError(
                f"Unsupported transform_type: {request.transform_type}. "
                f"Supported types: {supported}"
            )
        
        transform_func = transformations[request.transform_type]
        output_data = transform_func(request.input_data)
        
        return ProcessingResult(
            output_data=output_data,
            metadata={
                "transform_type": request.transform_type,
                "input_length": len(request.input_data),
                "output_length": len(output_data),
            },
        )

    def batch_process(self, inputs: list[str], transform_type: str = "uppercase") -> list[ProcessingResult]:
        """
        Process multiple inputs in batch.

        Args:
            inputs: List of input strings to process.
            transform_type: Type of transformation to apply to all inputs.

        Returns:
            List of ProcessingResult objects.
        """
        if self.verbose:
            logger.info(f"Batch processing {len(inputs)} items")

        results = []
        for input_data in inputs:
            result = self.process(input_data, transform_type)
            results.append(result)

        return results

    def get_stats(self) -> dict[str, Any]:
        """
        Get package statistics and information.

        Returns:
            Dictionary containing package statistics and configuration.
        """
        return {
            "version": "0.1.0",
            "verbose_mode": self.verbose,
            "settings": self.settings.model_dump(),
        }
