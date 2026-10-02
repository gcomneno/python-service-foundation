from fastapi import FastAPI
from fastapi.testclient import TestClient

from python_service_foundation.app import app


def test_application_is_fastapi_instance() -> None:
    assert isinstance(app, FastAPI)


def test_openapi_document_is_available() -> None:
    schema = app.openapi()

    assert schema["info"]["title"] == "Python Service Foundation"
    assert schema["info"]["version"] == "0.1.0"


def test_root_endpoint() -> None:
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"service": "python-service-foundation"}
