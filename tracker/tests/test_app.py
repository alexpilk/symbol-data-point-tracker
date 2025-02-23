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
