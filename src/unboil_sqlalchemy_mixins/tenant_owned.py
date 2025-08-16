from typing import TYPE_CHECKING
from typing_extensions import Self
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass
from sqlalchemy import ForeignKey, String


class TenantOwnedMixin(MappedAsDataclass):
    """
    SQLAlchemy 2.0 style mixin for multi-tenant applications.
    Inherit this class in your models to add a required, indexed 'tenant_id' column.

    Usage:
        
        class MyModel(TenantOwnedMixin, Base):
            ...

        class MyModel(TenantOwnedMixin.with_tenant_fk("tenants.id"), Base):
            ...
    """

    tenant_id: Mapped[str] = mapped_column(String, nullable=False, index=True)

    @staticmethod
    def with_tenant_fk(tenant_fk: str | None) -> type["TenantOwnedMixin"]:
        
        if tenant_fk is None:
            sqla_type = String()
        else:
            sqla_type = ForeignKey(tenant_fk, ondelete="CASCADE")
        
        class TenantOwnedMixinImpl(TenantOwnedMixin):
            tenant_id: Mapped[str] = mapped_column(sqla_type, nullable=False, index=True)

        return TenantOwnedMixinImpl
            