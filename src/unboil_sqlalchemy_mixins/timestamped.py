
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass
from sqlalchemy import DateTime, func

class TimestampedMixin(MappedAsDataclass):
    """
    SQLAlchemy 2.0 style mixin for timestamp fields.
    Inherit this class in your models to enable automatic timestamping.
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now(), init=False
    )