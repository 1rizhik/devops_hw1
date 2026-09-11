"""Тесты для API-сервиса модели."""
import pytest

from src.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'


def test_predict_valid(client):
    payload = {'features': [5.1, 3.5, 1.4, 0.2]}
    response = client.post('/predict', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'prediction' in data
    assert isinstance(data['prediction'], list)


def test_predict_setosa(client):
    payload = {'features': [5.1, 3.5, 1.4, 0.2]}
    response = client.post('/predict', json=payload)
    assert response.get_json()['prediction'][0] == 0


def test_predict_virginica(client):
    payload = {'features': [6.3, 3.3, 6.0, 2.5]}
    response = client.post('/predict', json=payload)
    assert response.get_json()['prediction'][0] == 2