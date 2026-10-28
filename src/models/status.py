from enum import StrEnum


class ProviderReservationStatus(StrEnum):
    """Статусы бронирования, определённые во внешнем AsyncAPI провайдеров."""

    AVAILABLE = "AVAILABLE"
    RESERVATION_PENDING = "RESERVATION_PENDING"
    RESERVED = "RESERVED"
    CANCELLATION_PENDING = "CANCELLATION_PENDING"
    CANCELLED = "CANCELLED"


class BookingStatus(StrEnum):
    """Внутреннее состояние всего составного бронирования."""

    PENDING = "PENDING"
    RESERVING = "RESERVING"
    RESERVED = "RESERVED"
    COMPENSATING = "COMPENSATING"
    COMPENSATED = "COMPENSATED"
    FAILED = "FAILED"


class OperationStatus(StrEnum):
    """Внутреннее состояние одной операции у конкретного провайдера."""

    PENDING = "PENDING"
    BOOKING_SENT = "BOOKING_SENT"
    BOOKED = "BOOKED"
    BOOKING_FAILED = "BOOKING_FAILED"
    CANCELLATION_SENT = "CANCELLATION_SENT"
    CANCELLED = "CANCELLED"
    CANCELLATION_FAILED = "CANCELLATION_FAILED"