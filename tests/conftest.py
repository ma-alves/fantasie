import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from fantasie.database import get_session
from fantasie.main import app
from fantasie.models import Base
from fantasie.security import get_password_hash

from factories import EmployeeFactory


@pytest.fixture
def test_session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
    )
    TestSession = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    yield TestSession()
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(test_session: Session):
    def get_session_override():
        return test_session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def employee(test_session: Session):
    password = 'test1234'
    new_employee = EmployeeFactory(password=get_password_hash(password))

    test_session.add(new_employee)
    test_session.commit()
    test_session.refresh(new_employee)

    new_employee.clean_password = 'test1234'

    return new_employee
