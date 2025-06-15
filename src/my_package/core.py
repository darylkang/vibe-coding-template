"""
Core business logic and models.

This module demonstrates modern Python patterns with Pydantic models
and clean architecture for LLM-assisted development.
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, Field

from my_package.settings import Settings

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class ProcessingRequest(BaseModel):
    """Request model for processing operations."""

    input_data: str = Field(..., description="Input data to be processed")
    transform_type: str = Field(
        default="uppercase",
        description="Type of transformation to apply",
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

    This class demonstrates clean architecture patterns and serves as
    the primary API for the package functionality.

    Example:
        >>> package = MyPackage()
        >>> result = package.process("hello world")
        >>> print(result.output_data)  # "HELLO WORLD"
    """

    def __init__(self, settings: Settings | None = None) -> None:
        """Initialize the package with optional settings."""
        self.settings = settings or Settings()
        logger.debug("MyPackage initialized")

    def process(
        self, input_data: str, transform_type: str = "uppercase"
    ) -> ProcessingResult:
        """
        Process input data with the specified transformation.

        Args:
            input_data: Raw input data to be processed.
            transform_type: Type of transformation to apply.

        Returns:
            ProcessingResult containing the processed data and metadata.
        """
        logger.info(f"Processing input with transform: {transform_type}")

        request = ProcessingRequest(
            input_data=input_data,
            transform_type=transform_type,
        )

        try:
            result = self._apply_transformation(request)
            logger.info("Processing completed successfully")
            return result

        except Exception as e:
            logger.error(f"Processing failed: {e}")
            return ProcessingResult(
                output_data="",
                success=False,
                metadata={"error": str(e)},
            )

    def _apply_transformation(self, request: ProcessingRequest) -> ProcessingResult:
        """Apply the requested transformation to the input data."""
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

    def get_stats(self) -> dict[str, Any]:
        """Get package statistics and information."""
        from my_package import __version__

        return {
            "version": __version__,
            "settings": self.settings.model_dump(),
        }
