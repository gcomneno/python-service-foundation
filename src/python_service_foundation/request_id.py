from contextvars import ContextVar
from uuid import uuid4

from starlette.types import ASGIApp, Message, Receive, Scope, Send

REQUEST_ID_HEADER = "X-Request-ID"
_REQUEST_ID_HEADER_BYTES = REQUEST_ID_HEADER.lower().encode("ascii")

_request_id_var: ContextVar[str | None] = ContextVar(
    "request_id",
    default=None,
)


def get_request_id() -> str | None:
    return _request_id_var.get()


def _is_valid_request_id(value: str) -> bool:
    if not 1 <= len(value) <= 128:
        return False

    return all(0x21 <= ord(character) <= 0x7E for character in value)


def _incoming_request_id(scope: Scope) -> str | None:
    headers = scope.get("headers", [])

    for name, value in headers:
        if name.lower() != _REQUEST_ID_HEADER_BYTES:
            continue

        try:
            decoded = value.decode("ascii")
        except UnicodeDecodeError:
            return None

        return decoded if _is_valid_request_id(decoded) else None

    return None


def _resolve_request_id(scope: Scope) -> str:
    incoming = _incoming_request_id(scope)

    if incoming is not None:
        return incoming

    return str(uuid4())


class RequestIdMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = _resolve_request_id(scope)
        token = _request_id_var.set(request_id)

        async def send_with_request_id(message: Message) -> None:
            if message["type"] == "http.response.start":
                headers = [
                    (name, value)
                    for name, value in message["headers"]
                    if name.lower() != _REQUEST_ID_HEADER_BYTES
                ]
                headers.append(
                    (
                        _REQUEST_ID_HEADER_BYTES,
                        request_id.encode("ascii"),
                    )
                )
                message["headers"] = headers

            await send(message)

        try:
            await self.app(
                scope,
                receive,
                send_with_request_id,
            )
        finally:
            _request_id_var.reset(token)
