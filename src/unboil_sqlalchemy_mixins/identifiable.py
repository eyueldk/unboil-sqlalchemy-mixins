from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass
from sqlalchemy import String
import uuid


class IdentifiableMixin(MappedAsDataclass):
    """
    Mixin for SQLAlchemy models to add a string 'id' primary key with optional user-specified prefix.
    Usage:
        class MyModel(IdentifiableMixin.with_config("user_"), Base):
            ...
    """

    id: Mapped[str] = mapped_column(
        String(32),
        primary_key=True,
        default_factory=lambda: uuid.uuid4().hex,
        nullable=False,
        init=False,
    )
    
    @classmethod
    def with_config(cls, prefix: str) -> "type[IdentifiableMixin]":
        class _IdentifiableMixin(IdentifiableMixin):
            id: Mapped[str] = mapped_column(
                String(32),
                primary_key=True,
                default_factory=lambda: f"{prefix}{uuid.uuid4().hex}",
                nullable=False,
                init=False,
            )
        return _IdentifiableMixin
    
    
IdentifiableMixin()