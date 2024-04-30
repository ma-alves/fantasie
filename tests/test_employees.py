from fastapi.testclient import TestClient


def test_read_employees(client: TestClient):
    response = client.get('/employees')
    assert response.status_code == 200
    assert response.json() == {'employees': []}


def test_create_employee(client: TestClient):
    response = client.post(
        '/employees',
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
        '/employees',
        json={
            'name': 'matheus',
            'email': 'matheus@email.com',
            'password': 'matheus1234',
            'phone_number': '12345678910'
        }
    )
    second_response = client.post(
        '/employees',
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


def test_read_employee(client: TestClient, employee):
    response = client.get(f'/employees/{employee.id}')
    assert response.status_code == 200
    assert response.json() == {
        'name': f'{employee.name}',
        'email': f'{employee.email}',
        'phone_number': f'{employee.phone_number}'
    }


def test_read_employee_not_registered(client: TestClient):
    response = client.get(f'/employees/404')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Employee not registered.'}
