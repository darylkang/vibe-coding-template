"""
Application settings and configuration management.

This module provides centralized configuration management using Pydantic Settings,
which automatically loads settings from environment variables, .env files, and
provides validation and type conversion.

INSTRUCTIONS FOR CURSOR:
- Add new settings as Pydantic fields with appropriate defaults
- Use environment variable names with the APP_ prefix
- Add validation methods for complex settings
- Document all settings with clear descriptions
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with environment variable support.

    This class uses Pydantic Settings to automatically load configuration
    from environment variables, .env files, and provide defaults.
    All settings can be overridden by environment variables with the APP_ prefix.

    Example:
        >>> settings = Settings()
        >>> settings.debug
        False
        >>> # Can be overridden with APP_DEBUG=true environment variable
    """

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application settings
    debug: bool = Field(
        default=False,
        description="Enable debug mode for verbose logging and error details",
    )

    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )

    # Processing settings
    default_transform: str = Field(
        default="uppercase",
        description="Default transformation type for processing operations",
    )

    max_batch_size: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Maximum number of items to process in a single batch",
    )

    # File and directory settings
    data_dir: Path = Field(
        default_factory=lambda: Path.cwd() / "data",
        description="Directory for storing data files",
    )

    output_dir: Path = Field(
        default_factory=lambda: Path.cwd() / "output",
        description="Directory for storing output files",
    )

    # Feature flags
    enable_rich_output: bool = Field(
        default=True, description="Enable Rich console output formatting"
    )

    enable_metrics: bool = Field(
        default=False, description="Enable metrics collection and reporting"
    )

    def __init__(self, **data: Any) -> None:
        """Initialize settings and create necessary directories."""
        super().__init__(**data)
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.debug or os.getenv("ENVIRONMENT", "").lower() in (
            "dev",
            "development",
        )

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return os.getenv("ENVIRONMENT", "").lower() in ("prod", "production")

    def get_log_config(self) -> dict[str, Any]:
        """Get logging configuration dictionary."""
        return {
            "level": self.log_level,
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            if not self.enable_rich_output
            else "%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
