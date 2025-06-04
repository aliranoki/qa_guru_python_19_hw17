from jsonschema import validate
import requests
from api_tests.schemas import get_all_users, get_single_user, post_user, get_created_user, put_user, register_user_successful, register_user_unsuccessful

endpoint = 'api/users/'
endpoint_register = 'api/register'

def test_get_users_list_on_page(url, headers):
    response = requests.get(f'{url}{endpoint}', params={"page": 1}, headers=headers)
    body = response.json()

    assert response.status_code == 200
    assert response.json()['per_page'] == 6
    validate(body, schema=get_all_users)

def test_get_single_user_by_id(url, headers):
    user_id = '9'
    response = requests.get(f'{url}{endpoint}{user_id}', headers=headers)
    body = response.json()

    assert response.status_code == 200
    assert body['data']['id'] == int(user_id)
    validate(body, schema=get_single_user)

def test_get_single_user_by_id_not_found(url, headers):
    user_id = '99'
    response = requests.get(f'{url}{endpoint}{user_id}', headers=headers)

    assert response.status_code == 404
    assert response.json() == {}

def test_create_user(url, headers):
    name = "Batman"
    job = "batman"

    payload = {
        "name": name,
        "job": job
    }
    response = requests.post(f'{url}{endpoint}', data=payload, headers=headers)
    body = response.json()

    assert response.status_code == 201
    assert body['name'] == name
    assert body['job'] == job
    validate(body, post_user)
    print(body)

def test_create_user_and_compare_request_vs_response_params(url, headers):
    email = "Batman@bat.man"
    first_name = "Bat"
    last_name = "man"
    avatar = "Batvatar"

    payload = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "avatar": avatar
    }
    response = requests.post(f'{url}{endpoint}', data=payload, headers=headers)
    body = response.json()

    assert response.status_code == 201
    assert body['first_name'] == first_name
    assert body['last_name'] == last_name
    assert body['email'] == email
    assert body['avatar'] == avatar
    validate(body, get_created_user)
    print(body)


def test_update_user_successful(url, headers):
    name = 'Superman'
    job = 'superman'
    id = '45'

    payload = {
        'name': name,
        'job': job
    }
    response = requests.put(f'{url}{endpoint}{id}', json=payload, headers=headers)
    body = response.json()

    assert response.status_code == 200
    assert body['name'] == name
    assert body['job'] == job
    validate(body, schema=put_user)
    print(body)


def test_delete_user(url, headers):
    id = '45'

    response = requests.delete(f'{url}{endpoint}{id}', headers=headers)

    assert response.status_code == 204
    assert response.text == ''

def test_get_deleted_user_by_id_not_found(url, headers):
    user_id = '45'

    response = requests.get(f'{url}{endpoint}{user_id}', headers=headers)

    assert response.status_code == 404
    assert response.json() == {}


def test_register_user_successful(url, headers):
    payload = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
    response = requests.post(f'{url}{endpoint_register}', data=payload, headers=headers)
    body = response.json()

    assert response.status_code == 200
    assert body["token"] is not None
    validate(body, register_user_successful)
    print(body)


def test_register_user_unsuccessful(url, headers):
    payload = {
        "email": "Batman@bat.man",
        "password": "joker_lox"
    }
    response = requests.post(f'{url}{endpoint_register}', json=payload, headers=headers)
    body = response.json()

    assert response.status_code == 400
    assert response.json()["error"] == "Note: Only defined users succeed registration"
    validate(body, register_user_unsuccessful)
    print(body)