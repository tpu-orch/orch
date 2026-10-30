from typing import Protocol
from uuid import UUID

from src.models.booking import Booking, BookingOperation
from src.models.payload import Payload
from src.models.provider import Provider
from src.models.status import BookingStatus, OperationStatus


class BookingRepository(Protocol):
    async def create(self, booking: Booking) -> Booking: ...

    async def update_operation_status(
        self,
        operation_id: UUID,
        status: OperationStatus,
    ) -> None: ...

    async def update_booking_status(
        self,
        composite_booking_id: int,
        status: BookingStatus,
    ) -> None: ...


class Orchestrator:
    def __init__(
        self,
        providers: list[Provider],
        repository: BookingRepository,
    ) -> None:
        self.providers: dict[str, Provider] = {}
        for provider in providers:
            if provider.name in self.providers:
                raise ValueError(f"Duplicate provider name: {provider.name}")
            self.providers[provider.name] = provider
        self.repository = repository

    async def run(self, payloads: list[Payload]) -> Booking:
        if not payloads:
            raise ValueError("A booking must contain at least one payload")

        for item in payloads:
            if item.name not in self.providers:
                raise ValueError(f"Unknown provider: {item.name}")

        booking = await self.repository.create(
            Booking(
                status=BookingStatus.RESERVING,
                operations=[
                    BookingOperation(
                        provider_name=item.name,
                        payload=item.payload,
                    )
                    for item in payloads
                ],
            )
        )
        if booking.composite_booking_id is None:
            raise ValueError("Repository did not assign a composite booking ID")

        for operation in booking.operations:
            provider = self.providers[operation.provider_name]
            operation.status = OperationStatus.BOOKING_SENT
            await self.repository.update_operation_status(
                operation.id,
                operation.status,
            )
            await provider.book(
                {
                    **operation.payload,
                    "compositeBookingId": booking.composite_booking_id,
                }
            )

        return booking
