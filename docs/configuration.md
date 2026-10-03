# Configuration

## Configuration model

Runtime configuration is defined in:

```text
src/python_service_foundation/config.py
```

The project uses `pydantic-settings`.

Environment variables use the prefix:

```text
PSF_
```

No automatic `.env` file loading is configured.

## Settings reference

### `PSF_SERVICE_NAME`

Purpose:

Defines the logical service name.

Default:

```text
python-service-foundation
```

Example:

```bash
export PSF_SERVICE_NAME=example-service
```

The service name is used by the FastAPI application and structured logging.

### `PSF_ENVIRONMENT`

Purpose:

Selects the runtime environment.

Default:

```text
development
```

Allowed values:

```text
development
test
staging
production
```

Example:

```bash
export PSF_ENVIRONMENT=production
```

Invalid values fail settings validation.

## Logging behavior by environment

The current logging level policy is:

| Environment | Level |
| --- | --- |
| `development` | `DEBUG` |
| `test` | `DEBUG` |
| `staging` | `INFO` |
| `production` | `INFO` |

There is intentionally no separate `PSF_LOG_LEVEL` setting.

## Local Compose configuration

The Compose development runtime supplies:

```text
PSF_ENVIRONMENT=development
PSF_SERVICE_NAME=python-service-foundation-compose
```

These values describe the local Compose runtime without altering application
source code.

## Direct container example

A production-oriented container can be started with:

```bash
docker run --rm \
  --publish 127.0.0.1:8000:8000 \
  --env PSF_ENVIRONMENT=production \
  --env PSF_SERVICE_NAME=python-service-foundation \
  python-service-foundation:local
```

## Secrets

The current foundation has no required secrets or credentials.

Future secrets must remain external to:

- source control;
- committed configuration;
- container images;
- deterministic test fixtures.

Provider credentials and downstream infrastructure configuration belong to the
milestones that introduce those dependencies, not to the foundation baseline.
