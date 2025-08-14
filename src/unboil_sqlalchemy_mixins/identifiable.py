from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass
from sqlalchemy import String
import uuid


class IdentifiableMixin(MappedAsDataclass):
    """
    Mixin for SQLAlchemy models to add a string 'id' primary key with optional user-specified prefix.
    Usage:
        class MyModel(IdentifiableMixin, Base, id_prefix="user_"):
            ...
    """

    id: Mapped[str]
    
    def __init_subclass__(cls, id_prefix: str = "") -> None:
        cls.id = mapped_column(
            String(32),
            primary_key=True,
            default_factory=lambda: f"{id_prefix}{uuid.uuid4().hex}",
            nullable=False,
            init=False,
        )