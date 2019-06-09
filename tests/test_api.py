import sys
sys.path.insert(0, '../src')
import json

import pytest

from src import api

@pytest.fixture
def client():
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.headers.get('Content-Type') == 'application/json'
    assert json.loads(response.data) == {'Status': 'OK'}

def test_allnews(client):
    response = client.get('/news')
    assert response.status_code == 200
    assert response.headers.get('Content-Type') == 'application/json'

    data = json.loads(response.data)
    # It should returns last 100 news
    assert len(data) == 100