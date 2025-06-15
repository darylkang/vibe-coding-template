"""
Test suite for the settings module.

This file provides comprehensive test coverage for the Settings class
and environment variable handling.
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from my_package.settings import Settings


class TestSettings:
    """Test cases for Settings class."""

    def test_default_settings(self) -> None:
        """Test default settings values."""
        settings = Settings()

        assert settings.debug is False
        assert settings.log_level == "INFO"
        assert settings.default_transform == "uppercase"
        assert settings.max_batch_size == 100
        assert settings.enable_rich_output is True
        assert settings.enable_metrics is False

    def test_custom_settings(self) -> None:
        """Test creating settings with custom values."""
        settings = Settings(
            debug=True,
            log_level="DEBUG",
            max_batch_size=50,
        )

        assert settings.debug is True
        assert settings.log_level == "DEBUG"
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

    def test_directory_creation(self, tmp_path: Path) -> None:
        """Test that directories are created during initialization."""
        data_dir = tmp_path / "test_data"
        output_dir = tmp_path / "test_output"

        Settings(
            data_dir=data_dir,
            output_dir=output_dir,
        )

        assert data_dir.exists()
        assert output_dir.exists()

    def test_batch_size_validation(self) -> None:
        """Test batch size validation constraints."""
        # Test minimum constraint
        with pytest.raises(ValueError):
            Settings(max_batch_size=0)

        # Test maximum constraint
        with pytest.raises(ValueError):
            Settings(max_batch_size=1001)

        # Test valid values
        settings = Settings(max_batch_size=1)
        assert settings.max_batch_size == 1

        settings = Settings(max_batch_size=1000)
        assert settings.max_batch_size == 1000

    @patch.dict(os.environ, {"ENVIRONMENT": "development"})
    def test_is_development(self) -> None:
        """Test development environment detection."""
        settings = Settings()
        assert settings.is_development is True

    @patch.dict(os.environ, {"ENVIRONMENT": "production"})
    def test_is_production(self) -> None:
        """Test production environment detection."""
        settings = Settings()
        assert settings.is_production is True

    @patch.dict(os.environ, {}, clear=True)
    def test_environment_defaults(self) -> None:
        """Test environment detection with no environment variables."""
        settings = Settings()
        assert settings.is_development is False
        assert settings.is_production is False

    def test_debug_implies_development(self) -> None:
        """Test that debug mode implies development environment."""
        settings = Settings(debug=True)
        assert settings.is_development is True

    def test_log_config_rich_enabled(self) -> None:
        """Test log configuration with Rich output enabled."""
        settings = Settings(enable_rich_output=True)
        config = settings.get_log_config()

        assert config["level"] == "INFO"
        assert config["format"] == "%(message)s"

    def test_log_config_rich_disabled(self) -> None:
        """Test log configuration with Rich output disabled."""
        settings = Settings(enable_rich_output=False)
        config = settings.get_log_config()

        assert config["level"] == "INFO"
        assert "%(asctime)s" in config["format"]

    def test_path_handling(self, tmp_path: Path) -> None:
        """Test that Path objects are handled correctly."""
        custom_data_dir = tmp_path / "custom_data"
        custom_output_dir = tmp_path / "custom_output"

        settings = Settings(
            data_dir=custom_data_dir,
            output_dir=custom_output_dir,
        )

        assert settings.data_dir == custom_data_dir
        assert settings.output_dir == custom_output_dir
        assert custom_data_dir.exists()
        assert custom_output_dir.exists()
