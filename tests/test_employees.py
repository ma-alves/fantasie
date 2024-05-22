from fastapi.testclient import TestClient

from fantasie.models import Employee


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
			'phone_number': '12345678910',
		},
	)
	assert response.status_code == 201
	assert response.json() == {
		'name': 'matheus',
		'email': 'matheus@email.com',
		'phone_number': '12345678910',
	}


def test_create_employee_already_exists(client: TestClient):
	first_response = client.post(
		'/employees',
		json={
			'name': 'matheus',
			'email': 'matheus@email.com',
			'password': 'matheus1234',
			'phone_number': '12345678910',
		},
	)
	second_response = client.post(
		'/employees',
		json={
			'name': 'matheus',
			'email': 'matheus@email.com',
			'password': 'matheus1234',
			'phone_number': '12345678910',
		},
	)
	assert first_response.status_code == 201
	assert second_response.status_code == 400
	assert second_response.json() == {'detail': 'Employee already registered.'}


def test_read_employee(client: TestClient, employee):
	response = client.get(f'/employees/{employee.id}')
	assert response.status_code == 200
	assert response.json() == {
		'name': f'{employee.name}',
		'email': f'{employee.email}',
		'phone_number': f'{employee.phone_number}',
	}


def test_read_employee_not_registered(client: TestClient):
	response = client.get(f'/employees/404')
	assert response.status_code == 404
	assert response.json() == {'detail': 'Employee not registered.'}


def test_update_employee(client: TestClient, employee: Employee, token: str):
	response = client.put(
		f'/employees/{employee.id}',
		headers={'Authorization': f'Bearer {token}'},
		json={
			'name': 'yasmim',
			'email': 'yasmim@email.com',
			'password': 'novasenha1234',
			'phone_number': '12345678910',
		},
	)
	assert response.status_code == 200
	assert response.json() == {
		'name': 'yasmim',
		'email': 'yasmim@email.com',
		'phone_number': '12345678910',
	}


def test_update_employee_no_permission(
	client: TestClient, employee: Employee, token: str
):
	response = client.put(
		f'/employees/400',
		headers={'Authorization': f'Bearer {token}'},
		json={
			'name': 'yasmim',
			'email': 'yasmim@email.com',
			'password': 'novasenha1234',
			'phone_number': '12345678910',
		},
	)
	assert response.status_code == 400
	assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_employee(client: TestClient, employee: Employee, token: str):
	response = client.delete(
		f'/employees/{employee.id}',
		headers={'Authorization': f'Bearer {token}'},
	)
	assert response.status_code == 200
	assert response.json() == {'message': 'Employee deleted.'}


def test_delete_employee_no_permission(
	client: TestClient, other_employee: Employee, token: str
):
	response_delete = client.delete(
		f'/employees/{other_employee.id}',
		headers={'Authorization': f'Bearer {token}'},
	)
	assert response_delete.status_code == 400
	assert response_delete.json() == {'detail': 'Not enough permissions'}
