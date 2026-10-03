# GiadaWare Python Service Foundation

**A minimal, audited production baseline for Python/FastAPI services.**

Technical repository/package name: `python-service-foundation`.

Informal shorthand: **PSF**.

A small, domain-neutral foundation for building production-minded Python HTTP
services.

## Status

Early learning-lab baseline. Public repository; v0.1.0 is the first tagged public release.

## Goals

- reproducible Python project setup;
- explicit package boundaries;
- automated formatting, linting, type checking, and tests;
- a minimal foundation that can later host an HTTP service;
- clean separation between reusable infrastructure and application domains.

## Non-goals

This foundation does not currently include:

- domain-specific models;
- external providers or provider SDKs;
- databases;
- Redis;
- caching policies;
- stale fallback;
- request coalescing;
- frontend code.

Those concerns belong to downstream applications or later milestones.

## Roadmap

The canonical project roadmap is maintained in [`docs/roadmap.md`](docs/roadmap.md).

## Development baseline

- Python 3.12+
- uv
- Ruff
- mypy
- pytest

Runtime HTTP dependencies will be introduced in later milestones.

## Local development with Docker Compose

The local development runtime uses Docker Compose and the production-oriented
Dockerfile. It intentionally runs a single application service without
database, Redis, reverse proxy, HTTPS, bind mounts, or persistent volumes.

Start the service:

```bash
docker compose up --build -d
```

Inspect service state:

```bash
docker compose ps
```

Verify the application:

```bash
curl http://127.0.0.1:8000/health/live
curl http://127.0.0.1:8000/health/ready
```

Inspect application logs:

```bash
docker compose logs app
```

After source changes, rebuild and restart with:

```bash
docker compose up --build -d
```

Stop the local runtime:

```bash
docker compose down
```

The Compose runtime does not define persistent application volumes, so
shutdown should not leave persistent application state behind.

## Quick start

Install the locked development environment:

```bash
uv sync --frozen --python 3.12
```

Run the validation suite:

```bash
uv lock --check
uv run --frozen ruff format --check .
uv run --frozen ruff check .
uv run --frozen mypy
uv run --frozen pytest -W error
```

Start the local container runtime:

```bash
docker compose up --build -d
```

Verify it:

```bash
curl http://127.0.0.1:8000/health/live
curl http://127.0.0.1:8000/health/ready
```

Stop it:

```bash
docker compose down
```

## HTTP surface

Versioned application API:

```text
/api/v1/
```

Operational endpoints:

```text
GET /health/live
GET /health/ready
```

Requests and responses support correlation through the `X-Request-ID` header.

## Project documentation

Detailed documentation is kept under `docs/`:

- [Architecture](docs/architecture.md) — application structure, routing,
  observability, runtime, and CI boundaries;
- [Development](docs/development.md) — setup, quality gates, tests, Docker, and
  Compose workflow;
- [Configuration](docs/configuration.md) — environment-variable reference and
  runtime configuration;
- [Design decisions](docs/decisions.md) — architecture choices and invariants;
- [Roadmap](docs/roadmap.md) — milestone state and acceptance criteria.

## Foundation boundary

Python Service Foundation is intentionally domain-neutral.

The foundation does not contain:

- sports-domain models;
- external sports-provider integration;
- provider credentials;
- database or Redis infrastructure;
- reverse proxy or TLS configuration;
- customer code, assets, payloads, or proprietary naming.

Those concerns belong to later milestones or downstream projects.

## Continuous integration

The repository includes a GitHub Actions validation workflow that enforces:

- lockfile consistency;
- frozen dependency installation;
- formatting;
- linting;
- strict static typing;
- tests with warnings treated as errors;
- Compose configuration validation;
- production-container build validation.

Third-party actions are pinned to immutable commit SHAs and the workflow uses
read-only repository permissions.
