from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass
from sqlalchemy import ForeignKey, String

class UserOwnedMixin(MappedAsDataclass):
    """
    SQLAlchemy 2.0 style mixin for multi-tenant applications.
    Inherit this class in your models to add a required, indexed 'user_id' column.

    Usage:
        class MyModel(UserOwnedMixin, Base):
            ...
        class MyModel(UserOwnedMixin, Base, user_fk="users.id"):
            ...
    """
    user_id: Mapped[str]

    def __init_subclass__(cls, user_fk: str | None = None) -> None:
        if user_fk is None:
            sqla_type = String()
        else:
            sqla_type = ForeignKey(user_fk, ondelete="CASCADE")
        cls.user_id = mapped_column(sqla_type, nullable=False, index=True)