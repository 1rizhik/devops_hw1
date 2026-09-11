"""Тесты для API-сервиса модели BankNote Authentication."""
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
    payload = {'features': [2.3718, 7.4908, 0.015989, -1.7414]}
    response = client.post('/predict', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'prediction' in data
    assert isinstance(data['prediction'], list)


def test_predict_authentic_banknote(client):
    """Подлинная банкнота — класс 0."""
    payload = {'features': [2.3718, 7.4908, 0.015989, -1.7414]}
    response = client.post('/predict', json=payload)
    assert response.get_json()['prediction'][0] == 0


def test_predict_fake_banknote(client):
    """Поддельная банкнота — класс 1."""
    payload = {'features': [-1.4446, 2.1438, -0.47241, -1.6677]}
    response = client.post('/predict', json=payload)
    assert response.get_json()['prediction'][0] == 1