FROM python:3.12-slim AS builder

ARG UV_VERSION=0.12.20

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN python -m pip install \
    --no-cache-dir \
    "uv==${UV_VERSION}"

COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src ./src

RUN uv sync \
    --frozen \
    --no-dev \
    --no-editable


FROM python:3.12-slim AS runtime

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd \
        --gid 10001 \
        app \
    && useradd \
        --uid 10001 \
        --gid 10001 \
        --no-create-home \
        --home-dir /nonexistent \
        --shell /usr/sbin/nologin \
        app

COPY --from=builder \
    --chown=10001:10001 \
    /app/.venv \
    /app/.venv

USER 10001:10001

EXPOSE 8000

CMD ["uvicorn", "python_service_foundation.app:app", "--host", "0.0.0.0", "--port", "8000"]
