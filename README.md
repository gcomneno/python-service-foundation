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
