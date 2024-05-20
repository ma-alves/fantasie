import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from fantasie.database import get_session
from fantasie.main import app
from fantasie.models import Base
from fantasie.security import get_password_hash

from factories import CostumeFactory, EmployeeFactory


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


@pytest.fixture
def other_employee(test_session: Session):
    password = 'test1234'
    new_employee = EmployeeFactory(password=get_password_hash(password))

    test_session.add(new_employee)
    test_session.commit()
    test_session.refresh(new_employee)

    new_employee.clean_password = 'test1234'

    return new_employee


@pytest.fixture
def token(client: TestClient, employee):
    response = client.post(
        '/auth/token',
        data={'username': employee.email, 'password': employee.clean_password},
    )
    return response.json()['access_token']


@pytest.fixture
def costume(test_session: Session):
    new_costume = CostumeFactory()

    test_session.add(new_costume)
    test_session.commit()
    test_session.refresh(new_costume)

    return new_costume
