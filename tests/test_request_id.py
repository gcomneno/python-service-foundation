import json
from concurrent.futures import ThreadPoolExecutor
from io import StringIO
from uuid import UUID

from fastapi import FastAPI
from fastapi.testclient import TestClient

from python_service_foundation.app import create_app
from python_service_foundation.config import Settings
from python_service_foundation.logging import configure_logging
from python_service_foundation.request_id import (
    REQUEST_ID_HEADER,
    RequestIdMiddleware,
    get_request_id,
)


def test_request_id_is_generated_when_missing() -> None:
    client = TestClient(create_app())

    response = client.get("/health/live")

    request_id = response.headers[REQUEST_ID_HEADER]

    UUID(request_id)

    assert response.status_code == 200
    assert request_id


def test_valid_incoming_request_id_is_preserved() -> None:
    client = TestClient(create_app())
    expected = "client-request-123"

    response = client.get(
        "/health/live",
        headers={REQUEST_ID_HEADER: expected},
    )

    assert response.status_code == 200
    assert response.headers[REQUEST_ID_HEADER] == expected


def test_invalid_incoming_request_id_is_replaced() -> None:
    client = TestClient(create_app())

    response = client.get(
        "/health/live",
        headers={REQUEST_ID_HEADER: "invalid request id"},
    )

    generated = response.headers[REQUEST_ID_HEADER]

    UUID(generated)

    assert generated != "invalid request id"


def test_request_id_is_available_to_structured_logs() -> None:
    stream = StringIO()
    application = create_app(
        Settings(
            service_name="request-id-test",
            environment="test",
        )
    )

    configure_logging(
        Settings(
            service_name="request-id-test",
            environment="test",
        ),
        stream=stream,
    )

    client = TestClient(application)
    expected = "trace-me-123"

    response = client.get(
        "/missing",
        headers={REQUEST_ID_HEADER: expected},
    )

    assert response.status_code == 404
    assert response.headers[REQUEST_ID_HEADER] == expected

    lines = stream.getvalue().splitlines()

    assert len(lines) == 1

    payload = json.loads(lines[0])

    assert payload["event"] == "http_error"
    assert payload["request_id"] == expected


def test_request_context_is_reset_after_request() -> None:
    client = TestClient(create_app())

    assert get_request_id() is None

    response = client.get(
        "/health/live",
        headers={REQUEST_ID_HEADER: "context-reset-test"},
    )

    assert response.status_code == 200
    assert get_request_id() is None


def test_concurrent_requests_do_not_share_request_ids() -> None:
    application = FastAPI()
    application.add_middleware(RequestIdMiddleware)

    @application.get("/request-id")
    async def request_id() -> dict[str, str | None]:
        return {"request_id": get_request_id()}

    def perform_request(request_id: str) -> tuple[str, str | None]:
        with TestClient(application) as client:
            response = client.get(
                "/request-id",
                headers={REQUEST_ID_HEADER: request_id},
            )

        assert response.status_code == 200

        return (
            response.headers[REQUEST_ID_HEADER],
            response.json()["request_id"],
        )

    ids = ("concurrent-a", "concurrent-b")

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(
            executor.map(
                perform_request,
                ids,
            )
        )

    assert results == [
        ("concurrent-a", "concurrent-a"),
        ("concurrent-b", "concurrent-b"),
    ]


def test_request_id_does_not_change_openapi_routes() -> None:
    application = create_app()

    assert sorted(application.openapi()["paths"]) == [
        "/api/v1/",
        "/health/live",
        "/health/ready",
    ]
