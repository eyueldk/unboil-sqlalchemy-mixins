
import pytest
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, MappedAsDataclass, Session
from unboil_sqlalchemy_mixins.identifiable import IdentifiableMixin

PREFIX = "example_"

class Base(MappedAsDataclass, DeclarativeBase):
    pass

class Example(IdentifiableMixin.with_config(PREFIX), Base):
    __tablename__ = "examples"
    name: Mapped[str] = mapped_column(String)

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_identifiable_mixin(session: Session):
    obj = Example(name="test")
    session.add(obj)
    session.commit()
    assert obj.id is not None
    assert obj.id.startswith(PREFIX)
