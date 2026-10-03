from typing import Annotated

from fastapi import FastAPI, Path
from fastapi.testclient import TestClient

from python_service_foundation.errors import ApplicationError
from python_service_foundation.http_errors import register_exception_handlers


def create_error_test_app() -> FastAPI:
    application = FastAPI()
    register_exception_handlers(application)

    @application.get("/application-error")
    async def application_error() -> None:
        raise ApplicationError(
            code="resource_not_found",
            message="Resource not found",
            status_code=404,
        )

    @application.get("/validated/{item_id}")
    async def validated(
        item_id: Annotated[int, Path(gt=0)],
    ) -> dict[str, int]:
        return {"item_id": item_id}

    return application


def test_application_error_uses_canonical_payload() -> None:
    client = TestClient(create_error_test_app())

    response = client.get("/application-error")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "resource_not_found",
            "message": "Resource not found",
        }
    }


def test_request_validation_error_uses_canonical_payload() -> None:
    client = TestClient(create_error_test_app())

    response = client.get("/validated/not-an-integer")

    assert response.status_code == 422
    assert response.json() == {
        "error": {
            "code": "validation_error",
            "message": "Request validation failed",
        }
    }


def test_framework_not_found_uses_canonical_payload() -> None:
    client = TestClient(create_error_test_app())

    response = client.get("/missing")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "not_found",
            "message": "Not Found",
        }
    }


def test_framework_method_not_allowed_uses_canonical_payload() -> None:
    client = TestClient(create_error_test_app())

    response = client.post("/validated/1")

    assert response.status_code == 405
    assert response.json() == {
        "error": {
            "code": "method_not_allowed",
            "message": "Method Not Allowed",
        }
    }
