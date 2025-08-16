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
    
        class MyModel(UserOwnedMixin.with_user_fk("users.id"), Base):
            ...
    """

    user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)

    @staticmethod
    def with_user_fk(user_fk: str | None) -> type["UserOwnedMixin"]:

        if user_fk is None:
            sqla_type = String()
        else:
            sqla_type = ForeignKey(user_fk, ondelete="CASCADE")

        class UserOwnedMixinImpl(UserOwnedMixin):
            user_id: Mapped[str] = mapped_column(sqla_type, nullable=False, index=True)

        return UserOwnedMixinImpl