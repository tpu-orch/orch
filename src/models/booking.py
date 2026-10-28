from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.models.status import (
    BookingStatus,
    OperationStatus,
    ProviderReservationStatus,
)


class BookingOperation(BaseModel):
    """Одна операция бронирования у выбранного провайдера."""

    id: UUID = Field(
        default_factory=uuid4,
        description="Внутренний идентификатор операции оркестратора.",
    )
    provider_name: str = Field(
        description="Имя провайдера, которому направляется операция.",
    )
    payload: dict[str, Any] = Field(
        description="Данные для провайдера",
    )
    status: OperationStatus = Field(
        default=OperationStatus.PENDING,
        description="Внутреннее состояние обработки операции.",
    )
    provider_status: ProviderReservationStatus | None = Field(
        default=None,
        description="Последний статус операции, полученный от провайдера.",
    )


class Booking(BaseModel):
    """Составное бронирование и состояние всех его операций."""

    composite_booking_id: int | None = Field(
        default=None,
        description="Идентификатор составного бронирования, созданный оркестратором.",
    )
    status: BookingStatus = Field(
        default=BookingStatus.PENDING,
        description="Внутреннее состояние всего составного бронирования.",
    )
    operations: list[BookingOperation] = Field(
        description="Операции бронирования, входящие в составное бронирование.",
    )
