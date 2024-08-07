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


def test_create_rental(
	client: TestClient, employee, token, available_costume, customer
):
	response = client.post(
		'/rental',
		headers={'Authorization': f'Bearer {token}'},
		json={
			'costume_id': available_costume.id,
			'customer_cpf': customer.cpf,
		},
	)
	assert response.status_code == 201
	assert response.json()['costume']['id'] == available_costume.id
	assert response.json()['customer']['cpf'] == customer.cpf
	assert response.json()['employee']['id'] == employee.id


def test_create_rental_unavailable_costume(
	client: TestClient, employee, token, unavailable_costume, customer
):
	response = client.post(
		'/rental',
		headers={'Authorization': f'Bearer {token}'},
		json={
			'costume_id': unavailable_costume.id,
			'customer_cpf': customer.cpf,
		},
	)
	assert response.status_code == 400
	assert response.json() == {'detail': 'Costume unavailable.'}


def test_create_rental_costume_not_registered(
	client: TestClient, employee, token, customer
):
	response = client.post(
		'/rental',
		headers={'Authorization': f'Bearer {token}'},
		json={'costume_id': -1, 'customer_cpf': customer.cpf},
	)
	assert response.status_code == 400
	assert response.json() == {'detail': 'Costume not registered.'}


def test_create_rental_customer_not_registered(
	client: TestClient, available_costume, employee, token
):
	response = client.post(
		'/rental',
		headers={'Authorization': f'Bearer {token}'},
		json={'costume_id': available_costume.id, 'customer_cpf': -1},
	)
	assert response.status_code == 400
	assert response.json() == {'detail': 'Customer not registered.'}


def test_patch_rental(client: TestClient, employee, token, rental):
	response = client.patch(
		f'/rental/{rental.id}',
		headers={'Authorization': f'Bearer {token}'},
		json={
			'rental_date': '2024-07-02T20:13:35.454321',
			'return_date': '2024-07-09T20:13:35.454321',
		},
	)
	assert response.status_code == 200
	assert response.json()['rental_date'] == '2024-07-02T20:13:35.454321'
	assert response.json()['return_date'] == '2024-07-09T20:13:35.454321'


def test_patch_rental_not_registered(client: TestClient, employee, token):
	response = client.patch(
		'/rental/404',
		headers={'Authorization': f'Bearer {token}'},
		json={
			'rental_date': '2024-07-02T20:13:35.454321',
			'return_date': '2024-07-09T20:13:35.454321',
		},
	)
	assert response.status_code == 404
	assert response.json() == {'detail': 'Rental not registered.'}


def test_patch_rental_wrong_datetime(
	client: TestClient, employee, token, rental
):
	response = client.patch(
		f'/rental/{rental.id}',
		headers={'Authorization': f'Bearer {token}'},
		json={
			'rental_date': '2024-07-02T20:13:35.454321',
			'return_date': '2024-07-01T20:13:35.454321',
		},
	)
	assert response.status_code == 400
	assert response.json() == {
		'detail': "Rental date can't be later than return date."
	}


def test_delete_rental(client: TestClient, employee, token, rental):
	response = client.delete(
		f'/rental/{rental.id}',
		headers={'Authorization': f'Bearer {token}'},
	)
	assert response.status_code == 200
	assert response.json() == {
		'message': 'Rental register has been deleted successfully.'
	}


def test_delete_rental_not_registered(client: TestClient, employee, token):
	response = client.delete(
		'/rental/404',
		headers={'Authorization': f'Bearer {token}'},
	)
	assert response.status_code == 404
	assert response.json() == {'detail': 'Rental not registered.'}
