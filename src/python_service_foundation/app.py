import logging

from fastapi import FastAPI

from python_service_foundation.api.v1.routes import router as v1_router
from python_service_foundation.config import Settings, get_settings
from python_service_foundation.health import router as health_router
from python_service_foundation.http_errors import register_exception_handlers
from python_service_foundation.logging import configure_logging, get_logger, log_event
from python_service_foundation.request_id import RequestIdMiddleware

logger = get_logger("app")


def create_app(settings: Settings | None = None) -> FastAPI:
    application_settings = settings or get_settings()

    configure_logging(application_settings)
    log_event(logger, logging.INFO, "service_configured")

    application = FastAPI(
        title=application_settings.service_name,
        version="0.1.0",
    )

    application.add_middleware(RequestIdMiddleware)

    application.dependency_overrides[get_settings] = lambda: application_settings
    register_exception_handlers(application)
    application.include_router(health_router)
    application.include_router(v1_router, prefix="/api/v1")

    return application


app = create_app()
