import pytest
from pydantic import ValidationError

from python_service_foundation.config import Settings, get_settings


def test_settings_defaults() -> None:
    settings = Settings()

    assert settings.service_name == "python-service-foundation"
    assert settings.environment == "development"


def test_service_name_environment_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PSF_SERVICE_NAME", "configured-service")

    settings = get_settings()

    assert settings.service_name == "configured-service"


def test_environment_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PSF_ENVIRONMENT", "staging")

    settings = get_settings()

    assert settings.environment == "staging"


def test_invalid_environment_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PSF_ENVIRONMENT", "invalid")

    with pytest.raises(ValidationError):
        get_settings()
