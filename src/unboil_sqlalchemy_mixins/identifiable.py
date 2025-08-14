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
    
        class MyModel(IdentifiableMixin, Base, id_prefix="user_"):
            ...
    """

    if TYPE_CHECKING:
        id: Mapped[str] = mapped_column(init=False)
    
    def __init_subclass__(cls, id_prefix: str = "", **kwargs):
        cls.id = mapped_column(
            String(32),
            primary_key=True,
            default=lambda: f"{id_prefix}{uuid.uuid4().hex}",
            nullable=False,
            init=False,
        )
        super().__init_subclass__(**kwargs)