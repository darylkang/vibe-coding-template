"""
Test suite for the settings module.

This file demonstrates basic settings testing patterns.
"""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from my_package.settings import Settings


class TestSettings:
    """Test cases for Settings configuration."""

    def test_default_settings(self) -> None:
        """Test default settings values."""
        settings = Settings()
        assert settings.debug is False
        assert settings.log_level == "INFO"
        assert settings.default_transform == "uppercase"
        assert settings.max_batch_size == 100

    def test_custom_settings(self) -> None:
        """Test creating settings with custom values."""
        settings = Settings(
            debug=True,
            log_level="DEBUG",
            default_transform="lowercase",
            max_batch_size=50,
        )
        assert settings.debug is True
        assert settings.log_level == "DEBUG"
        assert settings.default_transform == "lowercase"
        assert settings.max_batch_size == 50

    @patch.dict(
        os.environ,
        {
            "APP_DEBUG": "true",
            "APP_LOG_LEVEL": "WARNING",
            "APP_MAX_BATCH_SIZE": "200",
        },
    )
    def test_environment_variables(self) -> None:
        """Test loading settings from environment variables."""
        settings = Settings()
        assert settings.debug is True
        assert settings.log_level == "WARNING"
        assert settings.max_batch_size == 200

    def test_validation(self) -> None:
        """Test settings validation."""
        # Test minimum constraint
        with pytest.raises(ValueError):
            Settings(max_batch_size=0)

        # Test maximum constraint
        with pytest.raises(ValueError):
            Settings(max_batch_size=1001)
