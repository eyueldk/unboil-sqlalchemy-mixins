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

    user_id: Mapped[str] = mapped_column(String(), nullable=False, index=True)

    @classmethod
    def with_config(cls, user_fk: str) -> "type[UserOwnedMixin]":
        from sqlalchemy import ForeignKey
        class _UserOwnedMixin(UserOwnedMixin):
            user_id: Mapped[str] = mapped_column(
                ForeignKey(user_fk, ondelete="CASCADE"),
                nullable=False,
                index=True,
            )
        return _UserOwnedMixin