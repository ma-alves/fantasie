from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from fantasie.models import Costume, Customer, Employee, Rental

from factories import EmployeeFactory

def test_read_employees(client: TestClient):
    response = client.get('/employees/')
    assert response.status_code == 200
    assert response.json() == {'employees': []}


def test_create_employee(client: TestClient):
    response = client.post(
        '/employees/',
        json={
            'name': 'matheus',
            'email': 'matheus@email.com',
            'password': 'matheus1234',
            'phone_number': '12345678910'
        }
    )
    assert response.status_code == 201
    assert response.json() == {
        'name': 'matheus',
        'email': 'matheus@email.com',
        'phone_number': '12345678910'
    }


def test_create_employee_already_exists(client: TestClient):
    first_response = client.post(
        '/employees/',
        json={
            'name': 'matheus',
            'email': 'matheus@email.com',
            'password': 'matheus1234',
            'phone_number': '12345678910'
        }
    )
    second_response = client.post(
        '/employees/',
        json={
            'name': 'matheus',
            'email': 'matheus@email.com',
            'password': 'matheus1234',
            'phone_number': '12345678910'
        }
    )
    assert first_response.status_code == 201
    assert second_response.status_code == 400
    assert second_response.json() == {
        'detail': 'Employee already registered.'
    }
