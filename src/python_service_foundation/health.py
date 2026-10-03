from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

router = APIRouter()


def check_readiness() -> bool:
    return True


@router.get("/health/live")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness(
    ready: Annotated[bool, Depends(check_readiness)],
) -> JSONResponse:
    if not ready:
        return JSONResponse(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            content={"status": "not_ready"},
        )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"status": "ready"},
    )
