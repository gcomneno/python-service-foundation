import logging
from http import HTTPStatus
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from python_service_foundation.errors import ApplicationError
from python_service_foundation.logging import get_logger, log_event

logger = get_logger("http_errors")


def _error_payload(code: str, message: str) -> dict[str, dict[str, str]]:
    return {
        "error": {
            "code": code,
            "message": message,
        }
    }


def _http_error_code(status_code: int) -> str:
    if status_code == HTTPStatus.NOT_FOUND:
        return "not_found"

    if status_code == HTTPStatus.METHOD_NOT_ALLOWED:
        return "method_not_allowed"

    return "http_error"


def _http_error_message(status_code: int, detail: Any) -> str:
    if isinstance(detail, str):
        return detail

    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return "HTTP error"


async def application_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    del request

    if not isinstance(exc, ApplicationError):
        raise TypeError("unexpected exception type")

    log_event(
        logger,
        logging.WARNING,
        "application_error",
        code=exc.code,
        status_code=exc.status_code,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=_error_payload(exc.code, exc.message),
    )


async def request_validation_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    del request

    if not isinstance(exc, RequestValidationError):
        raise TypeError("unexpected exception type")

    log_event(
        logger,
        logging.WARNING,
        "request_validation_error",
        code="validation_error",
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
    )

    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content=_error_payload(
            "validation_error",
            "Request validation failed",
        ),
    )


async def http_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    del request

    if not isinstance(exc, StarletteHTTPException):
        raise TypeError("unexpected exception type")

    level = logging.INFO if exc.status_code < 500 else logging.WARNING

    log_event(
        logger,
        level,
        "http_error",
        code=_http_error_code(exc.status_code),
        status_code=exc.status_code,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=_error_payload(
            _http_error_code(exc.status_code),
            _http_error_message(exc.status_code, exc.detail),
        ),
        headers=exc.headers,
    )


def register_exception_handlers(application: FastAPI) -> None:
    application.add_exception_handler(
        ApplicationError,
        application_error_handler,
    )
    application.add_exception_handler(
        RequestValidationError,
        request_validation_error_handler,
    )
    application.add_exception_handler(
        StarletteHTTPException,
        http_exception_handler,
    )
