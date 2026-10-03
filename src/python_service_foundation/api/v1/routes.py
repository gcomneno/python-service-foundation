from typing import Annotated

from fastapi import APIRouter, Depends

from python_service_foundation.config import Settings, get_settings

router = APIRouter()


@router.get("/")
async def root(
    settings: Annotated[Settings, Depends(get_settings)],
) -> dict[str, str]:
    return {"service": settings.service_name}
