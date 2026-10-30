from uuid import UUID

from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncEngine

from src.models.booking import Booking, BookingOperation
from src.infra.db.tables import bookings, booking_operations
from src.models.status import BookingStatus, OperationStatus


class PostgresBookingRepository:
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    async def create(self, booking: Booking) -> Booking:
        async with self.engine.begin() as connection:
            result = await connection.execute(
                insert(bookings)
                .values(status=booking.status.value)
                .returning(bookings.c.composite_booking_id)
            )
            composite_booking_id = result.scalar_one()

            if booking.operations:
                await connection.execute(
                    insert(booking_operations),
                    [
                        {
                            "id": operation.id,
                            "composite_booking_id": composite_booking_id,
                            "provider_name": operation.provider_name,
                            "payload": operation.payload,
                            "status": operation.status.value,
                            "provider_status": (
                                operation.provider_status.value
                                if operation.provider_status
                                else None
                            ),
                        }
                        for operation in booking.operations
                    ],
                )

        return booking.model_copy(update={"composite_booking_id": composite_booking_id})

    async def update_operation_status(
        self,
        operation_id: UUID,
        status: OperationStatus,
    ) -> None:
        async with self.engine.begin() as connection:
            result = await connection.execute(
                update(booking_operations)
                .where(booking_operations.c.id == operation_id)
                .values(status=status.value)
            )
            if result.rowcount == 0:
                raise LookupError(f"Booking operation not found: {operation_id}")

    async def update_booking_status(
        self,
        composite_booking_id: int,
        status: BookingStatus,
    ) -> None:
        async with self.engine.begin() as connection:
            result = await connection.execute(
                update(bookings)
                .where(bookings.c.composite_booking_id == composite_booking_id)
                .values(status=status.value)
            )
            if result.rowcount == 0:
                raise LookupError(
                    f"Booking not found: {composite_booking_id}"
                )
