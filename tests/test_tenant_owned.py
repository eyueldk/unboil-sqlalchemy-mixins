import pytest
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, MappedAsDataclass, Session
from unboil_sqlalchemy_mixins import TenantOwnedMixin, UserOwnedMixin
from unboil_sqlalchemy_mixins.identifiable import IdentifiableMixin


class Base(MappedAsDataclass, DeclarativeBase):
    pass

class Tenant(Base):
    __tablename__ = "tenants"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)

class Example(IdentifiableMixin, TenantOwnedMixin, Base, tenant_fk="tenants.id"):
    __tablename__ = "examples"
    tenant_id: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()

def test_tenant_owned(session: Session):
    tenant = Tenant(id="t1", name="tenant1")
    session.add(tenant)
    session.commit()
    example = Example(name="example", tenant_id=tenant.id)
    session.add(example)
    session.commit()
    assert example.tenant_id == tenant.id
