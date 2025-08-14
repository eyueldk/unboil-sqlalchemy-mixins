from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass
from sqlalchemy import ForeignKey, String

class TenantOwnedMixin(MappedAsDataclass):
    """
    SQLAlchemy 2.0 style mixin for multi-tenant applications.
    Inherit this class in your models to add a required, indexed 'tenant_id' column.

    Usage:
        
        class MyModel(TenantOwnedMixin, Base):
            ...

        class MyModel(TenantOwnedMixin, Base, tenant_fk="tenants.id"):
            ...
    """

    if TYPE_CHECKING:
        tenant_id: Mapped[str]

    def __init_subclass__(cls, tenant_fk: str | None = None, **kwargs):
        if tenant_fk is None:
            sqla_type = String()
        else:
            sqla_type = ForeignKey(tenant_fk, ondelete="CASCADE")
        cls.tenant_id = mapped_column(sqla_type, nullable=False, index=True)
        super().__init_subclass__(**kwargs)