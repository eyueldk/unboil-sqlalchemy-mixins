import pytest
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, MappedAsDataclass, Session
from unboil_sqlalchemy_mixins.timestamped import TimestampedMixin
import time


class Base(MappedAsDataclass, DeclarativeBase):
    pass

class Example(TimestampedMixin, Base):
    __tablename__ = "example_timestamped"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()

def test_timestamped_fields(session: Session):
    obj = Example(id="test", name="foo")
    session.add(obj)
    session.commit()
    assert obj.created_at is not None
    assert obj.updated_at is not None
    # Check updated_at changes
    old_updated = obj.updated_at
    time.sleep(1)
    obj.name = "bar"
    session.commit()
    assert obj.updated_at > old_updated
