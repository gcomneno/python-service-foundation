import json
import logging
from datetime import UTC, datetime
from typing import TextIO

from python_service_foundation.config import Environment, Settings

LOGGER_NAME = "python_service_foundation"

_ENVIRONMENT_LEVELS: dict[Environment, int] = {
    "development": logging.DEBUG,
    "test": logging.DEBUG,
    "staging": logging.INFO,
    "production": logging.INFO,
}

_STRUCTURED_EXTRA_FIELDS = (
    "code",
    "status_code",
)


class JsonFormatter(logging.Formatter):
    def __init__(
        self,
        *,
        service: str,
        environment: Environment,
    ) -> None:
        super().__init__()
        self._service = service
        self._environment = environment

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(
            record.created,
            tz=UTC,
        ).isoformat(timespec="milliseconds")

        payload: dict[str, object] = {
            "timestamp": timestamp,
            "level": record.levelname,
            "logger": record.name,
            "event": getattr(record, "event", record.getMessage()),
            "service": self._service,
            "environment": self._environment,
        }

        for field in _STRUCTURED_EXTRA_FIELDS:
            value = getattr(record, field, None)

            if value is not None:
                payload[field] = value

        return json.dumps(
            payload,
            separators=(",", ":"),
            sort_keys=True,
        )


def configure_logging(
    settings: Settings,
    *,
    stream: TextIO | None = None,
) -> logging.Logger:
    level = _ENVIRONMENT_LEVELS[settings.environment]

    logger = logging.getLogger(LOGGER_NAME)
    logger.handlers.clear()
    logger.setLevel(level)
    logger.propagate = False

    handler = logging.StreamHandler(stream)
    handler.setLevel(level)
    handler.setFormatter(
        JsonFormatter(
            service=settings.service_name,
            environment=settings.environment,
        )
    )

    logger.addHandler(handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"{LOGGER_NAME}.{name}")


def log_event(
    logger: logging.Logger,
    level: int,
    event: str,
    *,
    code: str | None = None,
    status_code: int | None = None,
) -> None:
    extra: dict[str, object] = {
        "event": event,
    }

    if code is not None:
        extra["code"] = code

    if status_code is not None:
        extra["status_code"] = status_code

    logger.log(
        level,
        event,
        extra=extra,
    )
