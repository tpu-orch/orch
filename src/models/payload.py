from typing import Any

from pydantic import BaseModel, Field


class Payload(BaseModel):
    """Payload запроса на бронирование для одного провайдера."""

    name: str = Field(
        description="Имя провайдера, например avia или hotels.",
    )
    payload: dict[str, Any] = Field(
        description="Непрозрачные для оркестратора данные команды провайдеру.",
    )
