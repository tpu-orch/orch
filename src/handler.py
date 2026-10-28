from typing import Any

from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()


class Payload(BaseModel):
    name: str
    payload: dict[str, Any]


@router.post("/book", status_code=202)
async def composite_booking(payload: list[Payload]) -> dict[str, str]:
    # TODO
    return {"status": "accepted"}
