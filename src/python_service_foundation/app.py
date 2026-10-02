from fastapi import FastAPI

from python_service_foundation.config import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    application_settings = settings or get_settings()

    application = FastAPI(
        title=application_settings.service_name,
        version="0.1.0",
    )

    @application.get("/")
    async def root() -> dict[str, str]:
        return {"service": application_settings.service_name}

    return application


app = create_app()
