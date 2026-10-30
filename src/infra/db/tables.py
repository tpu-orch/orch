from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    MetaData,
    String,
    Table,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB

metadata = MetaData()

bookings = Table(
    "bookings",
    metadata,
    Column("composite_booking_id", BigInteger, primary_key=True, autoincrement=True),
    Column("status", String, nullable=False),
)

booking_operations = Table(
    "booking_operations",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column(
        "composite_booking_id",
        BigInteger,
        ForeignKey("bookings.composite_booking_id"),
        nullable=False,
    ),
    Column("provider_name", String, nullable=False),
    Column("payload", JSONB, nullable=False),
    Column("status", String, nullable=False),
    Column("provider_status", String),
)
