from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass
from sqlalchemy import ForeignKey, String

class TenantOwnedMixin(MappedAsDataclass):
    """
    SQLAlchemy 2.0 style mixin for multi-tenant applications.
    Inherit this class in your models to add a required, indexed 'tenant_id' column.

    Usage:
        class MyModel(TenantOwnedMixin, Base):
            ...
        class MyModel(TenantOwnedMixin.with_config("tenants.id"), Base):
            ...
    """

    tenant_id: Mapped[str] = mapped_column(String(), nullable=False, index=True)

    @classmethod
    def with_config(cls, tenant_fk: str) -> "type[TenantOwnedMixin]":
        from sqlalchemy import ForeignKey
        class _TenantOwnedMixin(TenantOwnedMixin):
            tenant_id: Mapped[str] = mapped_column(
                ForeignKey(tenant_fk, ondelete="CASCADE"),
                nullable=False,
                index=True,
            )
        return _TenantOwnedMixin