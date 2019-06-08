import pytest
import src.api as api

@pytest.fixture
def client():
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

def test_index(client):
    response = client.get('/')
    print(response)