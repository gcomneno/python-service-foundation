from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["development", "test", "staging", "production"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PSF_")

    service_name: str = "python-service-foundation"
    environment: Environment = "development"


def get_settings() -> Settings:
    return Settings()
