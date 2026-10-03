# Project Roadmap

## Purpose

This document is the canonical roadmap for the Python Service Foundation and
the downstream GiadaWare Sports Data Backend Lab.

The project is intentionally split into two layers:

1. a domain-neutral Python service foundation that may eventually be released
   publicly;
2. a sports-data learning lab built on top of that foundation.

The roadmap is organized so that each milestone introduces one primary
responsibility and leaves the system in a testable state.

## Status model

Milestones use the following states:

- `PLANNED` — accepted roadmap item, not yet started;
- `NEXT` — next milestone eligible for design and implementation;
- `IN_PROGRESS` — implementation has started but is not complete;
- `COMPLETE` — implementation, verification, and commit are complete;
- `BLOCKED` — progress requires an unresolved dependency or decision;
- `DEFERRED` — intentionally postponed.

A milestone is not `COMPLETE` merely because code exists. Completion requires
its acceptance criteria to pass and the resulting change to be committed.

## Current checkpoint

Current verified state:

- M0.1 — `COMPLETE`
- M0.2 — `COMPLETE`
- M0.3 — `COMPLETE`
- M0.4 — `NEXT`

The repository is still a private/local learning lab.

Public release has not been authorized.

---

# Layer 1 — Python Service Foundation

## Mission

Provide a small, domain-neutral foundation for production-minded Python HTTP
services.

The foundation should demonstrate explicit boundaries, reproducible
dependencies, typed configuration, HTTP conventions, observability,
containerization, automated quality gates, and deployment-oriented hygiene
without embedding any downstream application domain.

## M0.1 — Repository baseline

**Status:** `COMPLETE`

### Goal

Create a reproducible, typed Python project baseline.

### Scope

- Python 3.12+
- `pyproject.toml`
- `uv`
- `uv.lock`
- Hatchling
- `src/` layout
- `tests/`
- Ruff
- mypy strict
- pytest
- MIT license
- `.editorconfig`
- `.gitignore`

### Non-goals

- HTTP framework
- runtime service dependencies
- domain logic

### Acceptance criteria

- dependency synchronization succeeds;
- Ruff format check passes;
- Ruff lint passes;
- mypy strict passes;
- pytest passes;
- virtual environment and tool caches are ignored;
- repository has a clean initial commit.

### Verified commit

`5d5e147f4f5e70f2797124b51f7a2606809d1fd2`

---

## M0.2 — FastAPI application bootstrap

**Status:** `COMPLETE`

### Goal

Introduce the smallest runnable HTTP application boundary.

### Scope

- FastAPI;
- Uvicorn;
- application module;
- root HTTP endpoint;
- OpenAPI generation;
- HTTP contract tests;
- `httpx2` as a development-only test dependency.

### Non-goals

- configuration system;
- API versioning;
- health endpoints;
- logging;
- Docker.

### Acceptance criteria

- application imports successfully;
- application is a FastAPI instance;
- OpenAPI document is generated;
- root endpoint returns the expected neutral payload;
- test suite passes with warnings treated as errors.

### Verified commit

`723a3083536a390d755dd15625b9e9d350721976`

---

## M0.3 — Environment configuration

**Status:** `COMPLETE`

### Goal

Make service configuration explicit, typed, environment-driven, and testable.

### Scope

- `pydantic-settings`;
- `Settings`;
- `PSF_` environment-variable prefix;
- configurable service name;
- validated runtime environment;
- application factory accepting explicit settings.

### Configuration contract

Supported environments:

- `development`
- `test`
- `staging`
- `production`

Defaults:

- `service_name = "python-service-foundation"`
- `environment = "development"`

### Non-goals

- `.env` file loading;
- settings cache;
- global mutable configuration;
- secrets management.

### Acceptance criteria

- default settings work;
- environment overrides work;
- invalid environment values are rejected;
- application can be created with explicitly supplied settings;
- application metadata reflects supplied configuration;
- quality gates pass with warnings treated as errors.

### Verified commit

`f9ff6a3f3e967e6b9b60553ff4be0059fa85f5de`

---

## M0.4 — API routing and versioning

**Status:** `COMPLETE`

### Goal

Separate application bootstrap from the public HTTP surface and establish an
explicit API-version boundary.

### Planned scope

- API package;
- versioned router;
- `/api/v1` prefix;
- neutral demonstration endpoint moved behind the API router where
  appropriate;
- router-level tests.

### Non-goals

- canonical error model;
- health endpoints;
- sports domain;
- authentication;
- Redis.

### Acceptance criteria

- application bootstrap does not own feature routes directly;
- versioned API router is mounted explicitly;
- versioned route is visible in OpenAPI;
- routing tests pass;
- existing quality gates remain green.

### Verified commit

`880d77bf78f84e4fd589e16a940618333fd85667`

---

## M0.5 — Canonical HTTP and error model

**Status:** `COMPLETE`

### Goal

Define stable response and error conventions before downstream services depend
on them.

### Planned scope

- canonical error payload;
- application-specific error types;
- exception-to-HTTP mapping;
- validation/error contract tests.

### Non-goals

- provider-specific errors;
- Redis-specific errors;
- business-domain errors.

### Acceptance criteria

- known application errors map deterministically to HTTP responses;
- internal exception details are not leaked by default;
- error payload structure is documented and tested.

### Verified commit

`3e85a6275024ae2682a00b21913c59d15795de27`

---

## M0.6 — Liveness

**Status:** `COMPLETE`

### Goal

Provide a minimal process-liveness endpoint.

### Planned scope

- `/health/live`;
- no external dependency checks;
- deterministic HTTP contract.

### Acceptance criteria

- endpoint answers when the application process is healthy;
- endpoint does not depend on Redis, databases, providers, or external
  services.

### Verified commit

`a3411d31b0701cc8b9767c214d41fb8e342a687c`

---

## M0.7 — Readiness

**Status:** `COMPLETE`

### Goal

Provide a readiness boundary distinct from process liveness.

### Planned scope

- `/health/ready`;
- readiness model capable of incorporating future required dependencies;
- testable dependency-check abstraction.

### Acceptance criteria

- readiness semantics are distinct from liveness;
- readiness can fail without declaring the process dead;
- tests cover ready and not-ready states.

### Verified commit

`5ed195ce8fc1e37df99eb9d9b30fdcda8fc1fb9f`

---

## M0.8 — Structured logging

**Status:** `COMPLETE`

### Goal

Produce machine-readable, operationally useful logs.

### Planned scope

- structured application logs;
- consistent log fields;
- environment-aware logging configuration;
- explicit exception logging policy.

### Non-goals

- external log aggregation platform;
- vendor-specific observability SDK.

### Acceptance criteria

- application events are emitted in a stable structure;
- tests verify key logging behavior;
- secrets are not intentionally logged.

### Verified commit

`00ca2e8cc979d5b9f16401283b617159d2ca6c11`

---

## M0.9 — Correlation and request ID

**Status:** `COMPLETE`

### Goal

Make an HTTP request traceable through application logs.

### Planned scope

- request-ID middleware;
- incoming request-ID handling policy;
- generated IDs when missing;
- response propagation;
- logging integration.

### Acceptance criteria

- every request has a correlation identifier;
- identifier is available to logs;
- response exposes the agreed request-ID header;
- concurrent requests do not share identifiers accidentally.

### Verified commit

`f0c39e36b7263151fa6b8764e92589e12ad4cce8`

---

## M0.10 — Docker runtime

**Status:** `COMPLETE`

### Goal

Package the service into a reproducible production-oriented container image.

### Planned scope

- Dockerfile;
- Python runtime;
- dependency installation from locked state;
- non-root runtime user where practical;
- explicit command;
- graceful process lifecycle.

### Acceptance criteria

- image builds from a clean checkout;
- container starts successfully;
- HTTP service is reachable;
- tests or smoke checks verify the built image;
- development-only artifacts are not required at runtime.

### Verified commit

`a7f8f99dcba6659cd162c7f7007780226c469b1f`

---

## M0.11 — Compose development runtime

**Status:** `COMPLETE`

### Goal

Provide a reproducible local service runtime without introducing downstream
infrastructure prematurely.

### Planned scope

- Docker Compose service definition;
- local environment wiring;
- documented startup and shutdown flow.

### Non-goals

- Redis;
- database;
- reverse proxy;
- HTTPS.

### Acceptance criteria

- clean checkout can be started through documented Compose commands;
- service becomes reachable;
- shutdown leaves no unexpected persistent application state.

### Verified commit

`adf0c44ca77d0a94fd20acc216925654946f9ff1`

---

## M0.12 — CI hardening

**Status:** `COMPLETE`

### Goal

Move local quality gates into reproducible continuous integration.

### Planned scope

- GitHub Actions;
- pinned actions;
- `uv` frozen/locked dependency use;
- format check;
- lint;
- mypy strict;
- tests with warnings as errors;
- container/build checks where appropriate.

### Acceptance criteria

- CI reproduces local validation;
- CI does not depend on developer-machine state;
- dependency lockfile is enforced;
- permissions are minimized.

### Verified commit

`be22d603c6f5de8c6676d099f50ac0907051a874`

---

## M0.13 — Documentation and architecture

**Status:** `COMPLETE`

### Goal

Make the foundation understandable and reusable without requiring conversation
history.

### Planned scope

- README completion;
- architecture overview;
- development instructions;
- configuration reference;
- test/quality commands;
- runtime instructions;
- design decisions worth preserving.

### Acceptance criteria

- a new contributor can understand and run the project from repository
  documentation;
- public/private boundaries are documented;
- current architecture matches documentation.

### Verified commit

`ca03045c47f04620ac388d7fd1dad7860e2f5bd7`

---

## M0.14 — Clean-room and public-release audit

**Status:** `NEXT`

### Goal

Determine whether the foundation is safe and appropriate to publish as an
independent repository.

### Required gates

1. clean-room gate;
2. private-material gate;
3. secret/credential gate;
4. dependency and license gate;
5. documentation gate;
6. repository hygiene gate;
7. reproducible-build/test gate;
8. explicit public-release approval.

### Invariant

`M0 COMPLETE` does not imply `PUBLIC`.

Publication is allowed only after all release gates pass and publication is
explicitly approved.

---

# Layer 2 — GiadaWare Sports Data Backend Lab

## Mission

Build a clean-room sports-data backend learning lab on top of the Python
Service Foundation.

The lab should demonstrate operational backend engineering rather than merely
CRUD behavior.

Target architecture:

```text
provider
  -> adapter
  -> service
  -> cache/resilience
  -> REST API
  -> demo frontend
```

Raw provider-specific behavior must remain isolated from the public API and
domain model.

---

## M1 — Sports domain

**Status:** `PLANNED`

### Goal

Define a small synthetic sports domain independent of any external provider.

### Planned scope

Candidate concepts:

- league;
- team;
- match;
- score;
- match status.

### Constraints

- synthetic data first;
- no customer payloads;
- no provider-specific models;
- deterministic fixtures.

### Acceptance criteria

- domain models are provider-independent;
- synthetic fixtures cover normal and edge states;
- no network access is needed for domain tests.

---

## M2 — Provider architecture

**Status:** `PLANNED`

### Goal

Define a replaceable upstream-provider boundary.

### Planned scope

- provider protocol/interface;
- deterministic mock provider;
- provider-specific adapter boundary;
- provider error taxonomy.

### Acceptance criteria

- service code can operate against the mock;
- provider implementation can be replaced without changing the public REST
  contract;
- provider payloads do not leak into domain models.

---

## M3 — Service layer

**Status:** `PLANNED`

### Goal

Introduce application orchestration independent of HTTP transport and provider
implementation.

### Planned scope

- domain/application service;
- provider orchestration;
- service-level error semantics;
- unit tests without FastAPI.

### Acceptance criteria

- service layer does not depend on FastAPI request/response objects;
- service behavior is testable with mock dependencies;
- transport and provider boundaries remain separate.

---

## M4 — Redis cache

**Status:** `PLANNED`

### Goal

Introduce cache-aside behavior with explicit TTL semantics.

### Planned scope

- cache abstraction;
- Redis implementation;
- key namespace/versioning;
- serialization;
- fresh TTL behavior.

### Acceptance criteria

- cache hit avoids unnecessary provider request;
- cache miss invokes provider;
- fresh cached data is returned deterministically;
- Redis behavior has integration tests.

---

## M5 — Resilience

**Status:** `PLANNED`

### Goal

Provide controlled degradation when the upstream provider fails or becomes
slow.

### Planned scope

- provider timeout;
- fresh vs stale cache distinction;
- stale fallback;
- explicit upstream error when no usable cache exists;
- failure injection tests.

### Target behavior

```text
fresh cache
  -> return cached value

expired but stale-eligible
  -> attempt refresh
     -> success: return refreshed value
     -> failure: return stale value

no usable cached value
  -> provider failure
     -> explicit upstream error
```

### Acceptance criteria

- stale data is only returned inside the defined stale window;
- provider failure is distinguishable from successful fresh responses;
- retries do not create uncontrolled provider pressure.

---

## M6 — Single-flight and request coalescing

**Status:** `PLANNED`

### Goal

Prevent cache stampedes during concurrent misses or refreshes.

### Planned scope

- per-key refresh coordination;
- concurrent waiter behavior;
- error propagation;
- cancellation/timeout semantics.

### Acceptance criteria

- multiple simultaneous requests for the same missing key cause one effective
  upstream refresh;
- concurrent callers receive a consistent result;
- unrelated cache keys do not block one another;
- failure behavior is tested under concurrency.

---

## M7 — Observability

**Status:** `PLANNED`

### Goal

Make cache, provider, resilience, and concurrency behavior observable.

### Planned scope

- structured operational events;
- provider timing;
- cache outcome fields;
- stale/fresh indication;
- request correlation;
- essential metrics where useful.

### Acceptance criteria

Operators can distinguish at least:

- cache hit;
- cache miss;
- refresh;
- stale fallback;
- upstream failure;
- coalesced request.

---

## M8 — Real provider

**Status:** `PLANNED`

### Goal

Connect one public/free sports-data provider without weakening the clean-room
architecture.

### Preconditions

Provider integration must pass a preflight covering:

- availability;
- account eligibility;
- pricing/free quota;
- API access;
- relevant terms;
- structured response suitability;
- one controlled real call.

### Constraints

- mock provider remains canonical for deterministic tests;
- provider credentials never enter source control;
- provider adapter remains replaceable.

### Acceptance criteria

- real provider maps into existing domain models;
- public REST API does not change merely because the provider changes;
- tests can still run without live provider access.

---

## M9 — Production runtime

**Status:** `PLANNED`

### Goal

Package application and Redis into a production-oriented Docker deployment.

### Planned scope

- application container;
- Redis service;
- Docker Compose;
- environment configuration;
- restart behavior;
- persistent/runtime boundaries;
- operational smoke checks.

### Acceptance criteria

- stack starts from a clean environment;
- service and Redis communicate correctly;
- secrets remain external to images and repository;
- restart behavior is documented and tested where practical.

---

## M10 — Edge deployment

**Status:** `PLANNED`

### Goal

Expose the service safely through a production Linux edge.

### Planned scope

- reverse proxy;
- HTTPS/TLS;
- domain routing;
- proxy headers;
- deployment runbook;
- restart/update/troubleshooting instructions.

### Acceptance criteria

- HTTPS endpoint works;
- application is not unintentionally exposed outside the intended edge;
- proxy behavior preserves required request metadata;
- clean deployment procedure is documented.

---

## M11 — Demo client

**Status:** `PLANNED`

### Goal

Provide a deliberately small client that demonstrates backend behavior without
becoming a second product.

### Planned scope

Display enough information to demonstrate:

- normal data;
- fresh cache;
- refreshed data;
- stale fallback;
- explicit failure states where useful.

### Non-goals

- elaborate visual design;
- customer frontend reproduction;
- customer assets;
- full product UX.

### Acceptance criteria

- client consumes only the public REST API;
- no provider credentials reach the browser;
- frontend remains replaceable and independent from provider implementation.

---

# Cross-cutting invariants

The following rules apply throughout the roadmap.

## Clean-room

Do not use:

- customer code;
- customer assets;
- customer credentials;
- customer payloads copied as fixtures;
- proprietary naming or implementation details.

Requirements are rewritten as generic engineering problems.

## Dependency discipline

Introduce infrastructure only when a milestone requires it.

In particular, do not add technologies merely because they may eventually be
useful.

## Testability

Prefer boundaries that allow deterministic tests without:

- live networks;
- production accounts;
- external credentials;
- uncontrolled timing.

## Operational correctness

The project must distinguish business correctness from operational
correctness.

Examples of operational correctness include:

- bounded provider calls;
- cache semantics;
- controlled degradation;
- request coalescing;
- traceable failures;
- reproducible deployment.

## Evidence-first workflow

The canonical development flow is:

```text
EVIDENCE
  -> SCOPE
  -> DESIGN
  -> APPROVAL
  -> IMPLEMENT
  -> VERIFY
  -> COMMIT
```

No milestone is advanced solely because an implementation appears to work.

---

# Publication strategy

The Python Service Foundation is the primary candidate for independent public
release.

The Sports Data Backend Lab may also become public later, but only after a
separate clean-room and provider-license review.

The expected progression is:

```text
private learning lab
  -> technically complete foundation
  -> clean-room audit
  -> security/private-material audit
  -> dependency/license audit
  -> documentation audit
  -> explicit release approval
  -> public repository
```

No publication is automatic.
