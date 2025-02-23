import pytest
from fastapi.testclient import TestClient

from tracker.main import app, tracker

client = TestClient(app)


@pytest.fixture(autouse=True)
def fresh_tracker():
    tracker.reset()


@pytest.fixture
def nvda_3_points():
    client.post(
        '/add_batch', json={
            'symbol': 'NVDA',
            'values': [1.5, 2.0, 4.0]
        }
    )


def test_add_batch():
    response = client.post(
        '/add_batch', json={
            'symbol': 'NVDA',
            'values': [1.5, 2.0, 4.0]
        }
    )
    assert response.status_code == 201
    assert response.json() == {
        'data': {
            'symbol': 'NVDA',
            'points_added': 3,
        }
    }


def test_cannot_add_oversized_batch():
    response = client.post(
        '/add_batch', json={
            'symbol': 'NVDA',
            'values': list(range(10001))
        }
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {
                'type': 'too_long',
                'loc': ['body', 'values'],
                'msg': 'List should have at most 10000 items after validation, not 10001',
                'ctx': {
                    'field_type': 'List',
                    'max_length': 10000,
                    'actual_length': 10001
                }
            }
        ]
    }


def test_get_stats(nvda_3_points):
    response = client.get(
        '/stats', params={
            'symbol': 'NVDA',
            'k': 2
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'min': 1.5,
            'max': 4.0,
            'last': 4.0,
            'avg': 2.5,
            'var': pytest.approx(1.16666667)
        }
    }
