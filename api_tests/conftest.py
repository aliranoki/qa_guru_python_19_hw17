import pytest

@pytest.fixture()
def url():
    return 'https://reqres.in/'

@pytest.fixture
def headers():
    headers = {"x-api-key": "reqres-free-v1"}
    return headers