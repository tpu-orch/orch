from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.models.status import (
    BookingStatus,
    OperationStatus,
    ProviderReservationStatus,
)


class BookingOperation(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    provider_name: str
    payload: dict[str, Any]
    status: OperationStatus = OperationStatus.PENDING
    provider_status: ProviderReservationStatus | None = None


class Booking(BaseModel):
    composite_booking_id: int | None = None
    status: BookingStatus = BookingStatus.PENDING
    operations: list[BookingOperation]