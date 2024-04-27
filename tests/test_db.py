from sqlalchemy import select
from sqlalchemy.orm import Session

from fantasie.models import Costume, Customer, Employee, Rental


def test_create_costume(test_session: Session):
    new_costume = Costume(
        name='Batman',
        description='O homem morcego',
        fee=59.99,
        available=True
    )
    test_session.add(new_costume)
    test_session.commit()

    costume = test_session.scalar(
        select(Costume).where(new_costume.name == 'Batman')
    )

    assert costume.name == 'Batman'


def test_create_employee(test_session: Session):
    new_employee = Employee(
        name='Matheus',
        email='test@test.com',
        password='test',
        phone_number='00000000000'
    )
    test_session.add(new_employee)
    test_session.commit()

    employee = test_session.scalar(
        select(Employee).where(new_employee.email == 'test@test.com')
    )

    assert employee.email == 'test@test.com'
