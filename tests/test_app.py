from fastapi import FastAPI
from fastapi.testclient import TestClient

from python_service_foundation.app import app, create_app
from python_service_foundation.config import Settings


def test_application_is_fastapi_instance() -> None:
    assert isinstance(app, FastAPI)


def test_openapi_document_is_available() -> None:
    schema = app.openapi()

    assert schema["info"]["title"] == "python-service-foundation"
    assert schema["info"]["version"] == "0.1.0"


def test_root_endpoint() -> None:
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"service": "python-service-foundation"}


def test_application_uses_supplied_settings() -> None:
    configured_app = create_app(
        Settings(
            service_name="configured-service",
            environment="test",
        )
    )
    client = TestClient(configured_app)

    response = client.get("/")
    schema = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json() == {"service": "configured-service"}
    assert schema.json()["info"]["title"] == "configured-service"
