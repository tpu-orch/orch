from pydantic import BaseModel
from typing import Any


class Payload(BaseModel):
    name: str
    payload: dict[str, Any]
