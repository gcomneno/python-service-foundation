# Python Service Foundation

A small, domain-neutral foundation for building production-minded Python HTTP
services.

## Status

Early learning-lab baseline. Not yet approved for public release.

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
