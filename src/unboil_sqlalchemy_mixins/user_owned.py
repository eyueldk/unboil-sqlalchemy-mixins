from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass
from sqlalchemy import ForeignKey, String

class UserOwnedMixin(MappedAsDataclass):
    """
    SQLAlchemy 2.0 style mixin for user-owned models.
    Inherit this class in your models to add a required, indexed 'user_id' column.

    Usage:
    
        class MyModel(UserOwnedMixin, Base):
            ...
    
        class MyModel(UserOwnedMixin.with_config("users.id"), Base):
            ...
    """

    if TYPE_CHECKING:
        user_id: Mapped[str]

    def __init_subclass__(cls, user_fk: str | None = None, **kwargs):
        if user_fk is None:
            sqla_type = String()
        else:
            sqla_type = ForeignKey(user_fk, ondelete="CASCADE")
        cls.user_id = mapped_column(sqla_type, nullable=False, index=True)
        super().__init_subclass__(**kwargs)