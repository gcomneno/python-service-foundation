# Architecture

## Purpose

Python Service Foundation is a domain-neutral foundation for production-minded
Python HTTP services.

It provides reusable application, configuration, error-handling, health,
observability, container, local-runtime, and continuous-integration primitives
without introducing downstream domain or infrastructure concerns prematurely.

## Application assembly

The application entrypoint is:

```text
src/python_service_foundation/app.py
```

`create_app()` is the composition root.

It:

1. resolves application settings;
2. configures structured logging;
3. emits the initial `service_configured` event;
4. creates the FastAPI application;
5. installs request-ID middleware;
6. registers canonical exception handlers;
7. mounts operational health routes;
8. mounts the versioned API router under `/api/v1`.

The module also exposes:

```text
app = create_app()
```

for ASGI servers such as Uvicorn.

## Module boundaries

```text
python_service_foundation/
├── app.py
├── config.py
├── errors.py
├── health.py
├── http_errors.py
├── logging.py
├── request_id.py
└── api/
    └── v1/
        └── routes.py
```

Responsibilities:

- `app.py` — application composition;
- `config.py` — typed environment-based settings;
- `errors.py` — application-level error model;
- `http_errors.py` — translation into canonical HTTP error responses;
- `health.py` — liveness and readiness endpoints;
- `logging.py` — structured JSON application logging;
- `request_id.py` — request correlation middleware and context;
- `api/v1/routes.py` — versioned application API routes.

## HTTP routing

Application API routes are mounted below:

```text
/api/v1
```

Operational routes deliberately remain outside the versioned application API:

```text
/health/live
/health/ready
```

This keeps deployment and orchestration probes independent from application API
versioning.

## Error model

Known application and HTTP errors are translated into a canonical response
envelope:

```json
{
  "error": {
    "code": "example_code",
    "message": "Example message"
  }
}
```

Request validation errors are normalized rather than exposing raw framework
validation structures.

The foundation does not install a catch-all `Exception` handler. Unexpected
exceptions therefore remain distinguishable from explicitly modeled failures.

## Liveness and readiness

`GET /health/live` reports whether the application process is alive.

Successful response:

```json
{"status":"ok"}
```

`GET /health/ready` represents readiness to serve application traffic.

Successful response:

```json
{"status":"ready"}
```

A failed readiness check returns HTTP 503 with:

```json
{"status":"not_ready"}
```

The readiness dependency is replaceable through FastAPI dependency overrides,
which keeps readiness behavior deterministic in tests and extensible for future
infrastructure.

## Configuration

Configuration is defined with `pydantic-settings`.

Environment variables use the prefix:

```text
PSF_
```

The current settings are:

```text
PSF_SERVICE_NAME
PSF_ENVIRONMENT
```

See [configuration.md](configuration.md) for the complete reference.

## Structured logging

Application logging uses the Python standard library and emits JSON.

Core fields are:

```text
timestamp
level
logger
event
service
environment
```

When available, logs may also contain:

```text
request_id
code
status_code
```

Default logging levels are environment-dependent:

```text
development -> DEBUG
test        -> DEBUG
staging     -> INFO
production  -> INFO
```

No external logging framework is required.

## Request correlation

HTTP requests pass through a pure ASGI request-ID middleware.

Header:

```text
X-Request-ID
```

Behavior:

- a valid incoming request ID is preserved;
- a missing or invalid request ID is replaced with a generated UUID;
- the selected request ID is returned in the response header;
- the request ID is exposed to application logging through a `ContextVar`;
- request-local context is reset after completion;
- non-HTTP ASGI scopes bypass the middleware.

Accepted incoming values are 1–128 visible ASCII characters with no spaces or
control characters.

## Runtime architecture

The production-oriented image is defined by `Dockerfile`.

Build model:

```text
python:3.12-slim builder
  -> install pinned uv
  -> install locked runtime dependencies
  -> install project non-editably

python:3.12-slim runtime
  -> copy virtual environment only
  -> run as UID/GID 10001
  -> start Uvicorn on 0.0.0.0:8000
```

Development-only tools, tests, and documentation are not required by the final
runtime image.

## Compose development runtime

`compose.yaml` defines one application service.

Its current boundaries are intentional:

- one `app` service;
- host exposure only on `127.0.0.1:8000`;
- development environment configuration;
- liveness-based Compose healthcheck;
- 10-second stop grace period;
- no bind mounts;
- no persistent volumes;
- no database;
- no Redis;
- no reverse proxy;
- no HTTPS;
- no live-reload process.

Source changes therefore require rebuilding the image.

## Continuous integration

`.github/workflows/ci.yml` reproduces the local validation contract.

The workflow performs:

```text
uv lock --check
uv sync --frozen --python 3.12
uv run --frozen ruff format --check .
uv run --frozen ruff check .
uv run --frozen mypy
uv run --frozen pytest -W error
docker compose config
docker build --tag python-service-foundation:ci .
```

Third-party GitHub Actions are pinned to full commit SHAs.

Workflow permissions are limited to:

```yaml
contents: read
```

CI does not require repository secrets or publishing permissions.

## Current dependency direction

The current composition can be summarized as:

```text
environment
    |
    v
 Settings
    |
    v
create_app()
    |
    +--> structured logging
    |
    +--> request-ID middleware
    |
    +--> exception handlers
    |
    +--> health router
    |
    +--> /api/v1 router
```

The foundation intentionally contains no sports domain, provider integration,
database, Redis cache, reverse proxy, or public deployment infrastructure.
