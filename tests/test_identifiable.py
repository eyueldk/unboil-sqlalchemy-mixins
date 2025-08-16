
import pytest
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, MappedAsDataclass, Session
from unboil_sqlalchemy_mixins.identifiable import IdentifiableMixin

PREFIX = "example_"

class Base(MappedAsDataclass, DeclarativeBase):
    pass

class ExampleWithoutPrefix(IdentifiableMixin, Base):
    __tablename__ = "examples_without_prefix"
    name: Mapped[str] = mapped_column(String)

class ExampleWithPrefix(IdentifiableMixin.with_id_prefix(PREFIX), Base):
    __tablename__ = "examples_with_prefix"
    name: Mapped[str] = mapped_column(String)

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_identifiable_mixin_with_prefix(session: Session):
    obj = ExampleWithPrefix(name="test")
    session.add(obj)
    session.commit()
    assert obj.id is not None
    assert obj.id.startswith(PREFIX)

def test_identifiable_mixin_without_prefix(session: Session):
    obj = ExampleWithoutPrefix(name="test")
    session.add(obj)
    session.commit()
    assert obj.id is not None
    assert not obj.id.startswith(PREFIX)