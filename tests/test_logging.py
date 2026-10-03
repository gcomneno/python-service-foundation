import json
import logging
from io import StringIO
from typing import Annotated

from fastapi import FastAPI, Path
from fastapi.testclient import TestClient

from python_service_foundation.config import Environment, Settings
from python_service_foundation.errors import ApplicationError
from python_service_foundation.http_errors import register_exception_handlers
from python_service_foundation.logging import (
    LOGGER_NAME,
    configure_logging,
    get_logger,
    log_event,
)


def _decode_single_log(stream: StringIO) -> dict[str, object]:
    lines = stream.getvalue().splitlines()

    assert len(lines) == 1

    payload = json.loads(lines[0])

    assert isinstance(payload, dict)

    return payload


def _create_error_test_app() -> FastAPI:
    application = FastAPI()
    register_exception_handlers(application)

    @application.get("/application-error")
    async def application_error() -> None:
        raise ApplicationError(
            code="resource_not_found",
            message="super-secret-token",
            status_code=404,
        )

    @application.get("/validated/{item_id}")
    async def validated(
        item_id: Annotated[int, Path(gt=0)],
    ) -> dict[str, int]:
        return {"item_id": item_id}

    return application


def test_structured_log_has_stable_core_fields() -> None:
    stream = StringIO()
    settings = Settings(
        service_name="logging-test-service",
        environment="test",
    )

    configure_logging(settings, stream=stream)

    logger = get_logger("tests")
    log_event(logger, logging.INFO, "test_event")

    payload = _decode_single_log(stream)

    assert set(payload) == {
        "environment",
        "event",
        "level",
        "logger",
        "service",
        "timestamp",
    }
    assert payload["environment"] == "test"
    assert payload["event"] == "test_event"
    assert payload["level"] == "INFO"
    assert payload["logger"] == f"{LOGGER_NAME}.tests"
    assert payload["service"] == "logging-test-service"
    assert isinstance(payload["timestamp"], str)
    assert str(payload["timestamp"]).endswith("+00:00")


def test_logging_level_is_environment_aware() -> None:
    expected_levels: dict[Environment, int] = {
        "development": logging.DEBUG,
        "test": logging.DEBUG,
        "staging": logging.INFO,
        "production": logging.INFO,
    }

    for environment, expected_level in expected_levels.items():
        settings = Settings(environment=environment)
        logger = configure_logging(settings, stream=StringIO())

        assert logger.level == expected_level
        assert len(logger.handlers) == 1
        assert logger.handlers[0].level == expected_level


def test_application_error_log_is_structured_and_sanitized() -> None:
    stream = StringIO()
    configure_logging(
        Settings(environment="test"),
        stream=stream,
    )

    client = TestClient(_create_error_test_app())
    response = client.get("/application-error")

    assert response.status_code == 404

    payload = _decode_single_log(stream)

    assert payload["event"] == "application_error"
    assert payload["level"] == "WARNING"
    assert payload["code"] == "resource_not_found"
    assert payload["status_code"] == 404
    assert "super-secret-token" not in stream.getvalue()


def test_validation_error_log_does_not_include_raw_input() -> None:
    stream = StringIO()
    configure_logging(
        Settings(environment="test"),
        stream=stream,
    )

    client = TestClient(_create_error_test_app())
    response = client.get("/validated/raw-secret-input")

    assert response.status_code == 422

    payload = _decode_single_log(stream)

    assert payload["event"] == "request_validation_error"
    assert payload["level"] == "WARNING"
    assert payload["code"] == "validation_error"
    assert payload["status_code"] == 422
    assert "raw-secret-input" not in stream.getvalue()


def test_http_error_log_uses_controlled_fields() -> None:
    stream = StringIO()
    configure_logging(
        Settings(environment="test"),
        stream=stream,
    )

    client = TestClient(_create_error_test_app())
    response = client.get("/missing")

    assert response.status_code == 404

    payload = _decode_single_log(stream)

    assert payload["event"] == "http_error"
    assert payload["level"] == "INFO"
    assert payload["code"] == "not_found"
    assert payload["status_code"] == 404
    assert set(payload) == {
        "code",
        "environment",
        "event",
        "level",
        "logger",
        "service",
        "status_code",
        "timestamp",
    }
