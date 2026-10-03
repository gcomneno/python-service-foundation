from fastapi import FastAPI

from python_service_foundation.api.v1.routes import router as v1_router
from python_service_foundation.config import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    application_settings = settings or get_settings()

    application = FastAPI(
        title=application_settings.service_name,
        version="0.1.0",
    )

    application.dependency_overrides[get_settings] = lambda: application_settings
    application.include_router(v1_router, prefix="/api/v1")

    return application


app = create_app()
