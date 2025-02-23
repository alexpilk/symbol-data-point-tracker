import random

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
    return tracker


@pytest.fixture
def nvda_3_points(client):
    client.post(
        '/add_batch', json={
            'symbol': 'NVDA',
            'values': [1.5, 2.0, 4.0]
        }
    )


@pytest.fixture
def nvda_3_points_expected_stats():
    return {
        'data': {
            'min': 1.5,
            'max': 4.0,
            'last': 4.0,
            'avg': 2.5,
            'var': pytest.approx(1.16666667)
        }
    }


@pytest.fixture
def intl_5_points(client):
    client.post(
        '/add_batch', json={
            'symbol': 'INTL',
            'values': [5.0, 1.0, 7.9, 3.4, 0.1]
        }
    )


@pytest.fixture
def intl_5_points_expected_stats():
    return {
        'data': {
            'min': 0.1,
            'max': 7.9,
            'last': 0.1,
            'avg': pytest.approx(3.4799999999999995),
            'var': pytest.approx(7.885600000000001)
        }
    }


@pytest.fixture
def nvda_1e8_points(fresh_tracker):
    random.seed(0)
    fresh_tracker.add(
        'NVDA',
        values=[random.random() * 10 ** 4 for _ in range(10 ** 8)]
    )


@pytest.fixture
def nvda_1e7_points_expected_stats():
    return {
        'data': {
            'min': pytest.approx(0.0003373892532021472),
            'max': pytest.approx(9999.999134910702),
            'avg': pytest.approx(4999.9053275969645),
            'var': pytest.approx(8337202.862058624),
            'last': pytest.approx(5953.1932285127195)
        }
    }
