import pytest
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, MappedAsDataclass, Session
from unboil_sqlalchemy_mixins.user_owned import UserOwnedMixin


class Base(MappedAsDataclass, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)

class Example(UserOwnedMixin.with_user_fk("users.id"), Base):
    __tablename__ = "examples"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()

def test_user_owned(session: Session):
    user = User(id="u1", name="user1")
    session.add(user)
    session.commit()
    example = Example(id="exu1", name="example", user_id=user.id)
    session.add(example)
    session.commit()
    assert example.user_id == user.id
