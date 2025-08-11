from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
import uuid


class IdentifiableMixin:
    """
    Mixin for SQLAlchemy models to add a string 'id' primary key with a user-specified prefix.
    Usage:
        class MyModel(Identifiable.with_prefix('user_'), Base):
            ...
    """

    id: Mapped[str] = mapped_column(
        String(32), primary_key=True, default=uuid.uuid4().hex, nullable=False, init=False
    )

    @classmethod
    def with_prefix(cls, prefix: str):
        class _Identifiable(cls):
            id: Mapped[str] = mapped_column(
                String(32),
                primary_key=True,
                default=lambda: f"{prefix}{uuid.uuid4().hex}",
                nullable=False,
            )

        return _Identifiable
