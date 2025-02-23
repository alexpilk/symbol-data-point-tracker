import pytest
from fastapi.testclient import TestClient

from tracker.api import app
from tracker.service import tracker


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def fresh_tracker():
    tracker.reset()


@pytest.fixture
def nvda_3_points(client):
    client.post(
        '/add_batch', json={
            'symbol': 'NVDA',
            'values': [1.5, 2.0, 4.0]
        }
    )
