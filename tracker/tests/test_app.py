from fastapi.testclient import TestClient

from tracker.main import app

client = TestClient(app)


def test_add_batch():
    response = client.post(
        '/add_batch', json={
            'symbol': 'NVDA',
            'values': [1, 2, 4]
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
