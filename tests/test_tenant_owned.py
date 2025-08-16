import pytest
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, MappedAsDataclass, Session
from unboil_sqlalchemy_mixins import TenantOwnedMixin, UserOwnedMixin
from unboil_sqlalchemy_mixins.identifiable import IdentifiableMixin


class Base(MappedAsDataclass, DeclarativeBase):
    pass

class Tenant(IdentifiableMixin, Base):
    __tablename__ = "tenants"
    name: Mapped[str] = mapped_column(String)

class ExampleWithoutFK(IdentifiableMixin, TenantOwnedMixin, Base):
    __tablename__ = "examples_without_fk"
    name: Mapped[str] = mapped_column(String)

class ExampleWithFK(IdentifiableMixin, TenantOwnedMixin.with_tenant_fk("tenants.id"), Base):
    __tablename__ = "examples_with_fk"
    name: Mapped[str] = mapped_column(String)

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()

def test_tenant_owned_with_fk(session: Session):
    tenant = Tenant(name="tenant1")
    session.add(tenant)
    session.commit()
    example = ExampleWithoutFK(name="example", tenant_id=tenant.id)
    session.add(example)
    session.commit()
    assert example.tenant_id == tenant.id


def test_tenant_owned_without_fk(session: Session):
    tenant_id = "default"
    example = ExampleWithoutFK(name="example", tenant_id=tenant_id)
    session.add(example)
    session.commit()
    assert example.tenant_id == tenant_id