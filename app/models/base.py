from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


def utc_now():
    """
    Возвращает текущий момент времени в UTC
    в виде timezone-aware datetime.
    """
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    """Базовый класс всех моделей."""

    @declared_attr
    def id(cls) -> Mapped[int]:
        return mapped_column(primary_key=True)

    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            default=utc_now,
            nullable=False,
        )

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(
            DateTime(timezone=True),
            default=utc_now,
            onupdate=utc_now,
            nullable=False,
        )
