from fastapi.testclient import TestClient

from fantasie.routes.rental import set_rental_attr


def test_read_rental(client: TestClient, employee, token, rental):
	response = client.get(
		f'/rental/{rental.id}',
		headers={'Authorization': f'Bearer {token}'},
	)
	set_rental_attr(rental)

	assert response.status_code == 200
	assert response.json()['costume']['id'] == rental.costumes.id
	assert response.json()['customer']['cpf'] == rental.customers.cpf


def test_read_rental_not_registered(client: TestClient, employee, token):
	response = client.get(
		'/rental/404',
		headers={'Authorization': f'Bearer {token}'},
	)
	assert response.status_code == 404
	assert response.json() == {'detail': 'Rental not registered.'}


def test_read_rental_list(client: TestClient, employee, token):
	response = client.get(
		'/rental',
		headers={'Authorization': f'Bearer {token}'},
	)
	assert response.status_code == 200
	assert response.json() == {'rental_list': []}


def test_create_rental(client: TestClient, employee, token, available_costume, customer):
	response = client.post(
		'/rental',
		headers={'Authorization': f'Bearer {token}'},
		json={
			'costume_id': available_costume.id,
			'customer_cpf': customer.cpf
		}
	)
	print(response.json())
	assert response.status_code == 201
	assert response.json()['costume']['id'] == available_costume.id
	assert response.json()['customer']['cpf'] == customer.cpf
	assert response.json()['employee']['id'] == employee.id


# test create rental errors