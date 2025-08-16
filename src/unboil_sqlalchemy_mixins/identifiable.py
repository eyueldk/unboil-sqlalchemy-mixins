from typing import TYPE_CHECKING, Any, Callable, Type
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass
from sqlalchemy import String
import uuid

from sqlalchemy.sql.base import _NoArg


class IdentifiableMixin(MappedAsDataclass):
    """
    Mixin for SQLAlchemy models to add a string 'id' primary key with optional user-specified prefix.
    Usage:

        class MyModel(IdentifiableMixin, Base):
            ...

        class MyModel(IdentifiableMixin.with_id_prefix("user_"), Base):
            ...
    """

    id: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
        default=lambda: uuid.uuid4().hex,
        nullable=False,
        init=False,
    )

    @staticmethod
    def with_id_prefix(id_prefix: str) -> type["IdentifiableMixin"]:
        class IdentifiableMixinImpl(IdentifiableMixin):
            id: Mapped[str] = mapped_column(
                String(255),
                primary_key=True,
                default=lambda: f"{id_prefix}{uuid.uuid4().hex}",
                nullable=False,
                init=False,
            )
        return IdentifiableMixinImpl