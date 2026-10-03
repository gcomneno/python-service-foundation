from fastapi.testclient import TestClient

from python_service_foundation.app import app, create_app
from python_service_foundation.health import check_readiness


def test_liveness_endpoint_returns_ok() -> None:
    client = TestClient(app)

    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_liveness_endpoint_is_available_outside_api_version_prefix() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/health/live")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "not_found",
            "message": "Not Found",
        }
    }


def test_readiness_endpoint_returns_ready() -> None:
    client = TestClient(app)

    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_readiness_can_fail_without_failing_liveness() -> None:
    application = create_app()
    application.dependency_overrides[check_readiness] = lambda: False
    client = TestClient(application)

    readiness_response = client.get("/health/ready")
    liveness_response = client.get("/health/live")

    assert readiness_response.status_code == 503
    assert readiness_response.json() == {"status": "not_ready"}

    assert liveness_response.status_code == 200
    assert liveness_response.json() == {"status": "ok"}


def test_readiness_endpoint_is_available_outside_api_version_prefix() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/health/ready")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "not_found",
            "message": "Not Found",
        }
    }
