# Development

## Prerequisites

The development baseline requires:

- Python 3.12 or newer;
- `uv`;
- Docker Engine;
- Docker Compose.

The repository commits `uv.lock`, which is part of the reproducibility
contract.

## Install the development environment

From the repository root:

```bash
uv sync --frozen --python 3.12
```

The frozen installation prevents dependency resolution from silently changing
the committed lock state.

## Lockfile verification

Verify that the lockfile matches project metadata:

```bash
uv lock --check
```

A lock mismatch is a validation failure.

## Formatting

Check formatting without modifying files:

```bash
uv run --frozen ruff format --check .
```

## Linting

Run Ruff lint checks:

```bash
uv run --frozen ruff check .
```

## Static typing

Run strict mypy validation:

```bash
uv run --frozen mypy
```

The project enables strict mypy mode for `src` and `tests`.

## Tests

Run the test suite with warnings promoted to errors:

```bash
uv run --frozen pytest -W error
```

Tests are designed to avoid reliance on uncontrolled live services.

## Canonical local validation

Before committing a milestone implementation, the current quality sequence is:

```bash
uv lock --check
uv run --frozen ruff format --check .
uv run --frozen ruff check .
uv run --frozen mypy
uv run --frozen pytest -W error
docker compose config
```

When container changes are involved, also build the production-oriented image:

```bash
docker build --tag python-service-foundation:local-check .
```

The temporary image may be removed after validation:

```bash
docker image rm python-service-foundation:local-check
```

## Run with Docker Compose

Build and start the local service:

```bash
docker compose up --build -d
```

Inspect status:

```bash
docker compose ps
```

Check liveness:

```bash
curl http://127.0.0.1:8000/health/live
```

Check readiness:

```bash
curl http://127.0.0.1:8000/health/ready
```

Inspect logs:

```bash
docker compose logs app
```

Stop the runtime:

```bash
docker compose down
```

The Compose configuration defines no persistent application volumes.

## Source changes

The current Compose runtime deliberately has no source bind mount and no reload
process.

After changing source code, rebuild:

```bash
docker compose up --build -d
```

This favors reproducibility over live-edit convenience.

## Run the production-oriented container directly

Build:

```bash
docker build --tag python-service-foundation:local .
```

Run:

```bash
docker run --rm \
  --publish 127.0.0.1:8000:8000 \
  --env PSF_ENVIRONMENT=production \
  python-service-foundation:local
```

The runtime image starts Uvicorn explicitly and runs as a non-root user.

## Continuous integration

The GitHub Actions workflow is:

```text
.github/workflows/ci.yml
```

It reproduces the repository's local validation sequence using:

- pinned GitHub Actions;
- pinned `uv`;
- Python 3.12;
- frozen dependency installation;
- format, lint, mypy, and pytest checks;
- Compose configuration validation;
- Docker image build validation.

The workflow requires read-only repository contents permission.

## Development workflow

The canonical engineering sequence is:

```text
EVIDENCE
  -> SCOPE
  -> DESIGN
  -> APPROVAL
  -> IMPLEMENT
  -> VERIFY
  -> COMMIT
```

A milestone is not advanced solely because the implementation appears to work.
The corresponding acceptance criteria and invariants must also be verified.
