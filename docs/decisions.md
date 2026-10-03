# Design decisions

## Project identity

The public project name is **GiadaWare Python Service Foundation**.

The stable technical repository/package name remains
`python-service-foundation`.

**PSF** is the informal shorthand used when context is unambiguous.

The public positioning line is:

> A minimal, audited production baseline for Python/FastAPI services.

The branding decision does not alter package imports, runtime configuration,
container behavior, API contracts, or the clean-room boundary.

This document records architecture decisions that are important to preserve when
the foundation is reused or extended.

## Python 3.12 baseline

The package requires Python 3.12 or newer.

Tool configuration also targets Python 3.12 so runtime, linting, typing, tests,
and CI share the same baseline.

## `uv` and committed lockfile

`uv` is the dependency-management tool.

`uv.lock` is committed and validation uses frozen or explicit lock checks.

Rationale:

- reproducible dependency state;
- consistent local and CI behavior;
- dependency drift becomes visible.

## Hatchling build backend

The project uses Hatchling as its Python build backend.

The package is built from:

```text
src/python_service_foundation
```

## FastAPI application factory

Application construction lives in `create_app()`.

Rationale:

- settings can be injected in tests;
- application composition is explicit;
- framework wiring is centralized.

## Environment-based typed settings

Configuration uses `pydantic-settings` with the `PSF_` prefix.

The foundation does not automatically load `.env` files.

Rationale:

- runtime configuration remains explicit;
- container and CI behavior does not depend on local hidden files;
- configuration validation stays typed.

## Versioned application API

Application routes live below:

```text
/api/v1
```

Operational health endpoints remain outside that prefix.

Rationale:

- application API evolution and operational probes have different lifecycles;
- deployment health checks should not depend on domain API versioning.

## Canonical HTTP errors

Known failures use a stable application-owned error envelope.

Framework validation details are normalized instead of being exposed directly.

Unexpected exceptions are not hidden by a global catch-all handler.

Rationale:

- clients receive a predictable contract;
- framework internals do not define the public error model;
- unexpected failures remain operationally visible.

## Separate liveness and readiness

The foundation exposes:

```text
/health/live
/health/ready
```

Readiness has an injectable dependency boundary.

Rationale:

- process liveness and traffic readiness are different operational states;
- future infrastructure dependencies can extend readiness without changing the
  liveness contract;
- deterministic tests remain possible.

## Standard-library structured logging

Structured logs use Python `logging` plus a JSON formatter.

No external logging dependency is required.

Rationale:

- minimal dependency surface;
- stable machine-readable events;
- application-controlled structured fields.

## Pure ASGI request-ID middleware

Request correlation is implemented at the ASGI boundary.

Rationale:

- request IDs cover the complete HTTP request lifecycle;
- correlation context is available to application logging;
- middleware remains independent from domain handlers;
- concurrent requests are isolated through `ContextVar`.

## Docker multi-stage runtime

The Dockerfile uses a builder and a separate slim runtime stage.

Only locked runtime dependencies and the installed package enter the final
runtime environment.

The runtime user is non-root with UID/GID 10001.

Rationale:

- development dependencies are excluded;
- source tree and test suite are not required at runtime;
- runtime privileges are reduced.

## No Dockerfile healthcheck

The image itself does not define a Docker `HEALTHCHECK`.

Health policy is currently defined by the deployment/runtime layer through
Compose.

Rationale:

- the image exposes health endpoints;
- probe cadence and operational policy belong to the runtime environment.

## Compose is a reproducible runtime, not live editing

The development Compose configuration has:

- one application service;
- loopback-only host binding;
- no bind mounts;
- no persistent volumes;
- no reload mode.

Rationale:

- local runtime behavior remains close to the built image;
- host filesystem state does not silently affect execution;
- source changes require an explicit rebuild.

## Infrastructure is introduced only when required

The foundation currently excludes:

- database;
- Redis;
- reverse proxy;
- HTTPS termination;
- external provider integration.

Rationale:

- avoid premature coupling;
- keep the foundation reusable;
- make each future infrastructure dependency correspond to an explicit
  milestone and acceptance contract.

## CI reproduces local validation

Continuous integration executes the same core checks used locally.

Third-party actions are pinned to full commit SHAs.

Permissions are read-only and action caching is disabled.

Rationale:

- mutable action tags are avoided;
- unnecessary write capability is removed;
- CI behavior is explicit and easier to audit;
- correctness does not depend on developer-machine state.

## Clean-room boundary

The foundation is domain-neutral.

It must not incorporate:

- customer code;
- customer assets;
- customer credentials;
- copied customer payloads;
- proprietary naming;
- downstream sports-provider implementation details.

Requirements are expressed as generic engineering problems.

A separate release audit determines whether the repository is suitable for
public publication.
