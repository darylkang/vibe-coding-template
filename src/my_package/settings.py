"""
Simple settings management with Pydantic Settings.

This module demonstrates basic configuration patterns for modern Python applications.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with environment variable support.

    Example:
        >>> settings = Settings()
        >>> settings.debug  # False by default
        >>> # Can be overridden with APP_DEBUG=true environment variable
    """

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Basic application settings
    debug: bool = Field(default=False, description="Enable debug mode")

    log_level: str = Field(default="INFO", description="Logging level")

    # Processing settings
    default_transform: str = Field(
        default="uppercase", description="Default text transformation"
    )

    max_batch_size: int = Field(
        default=100, ge=1, le=1000, description="Maximum batch processing size"
    )
