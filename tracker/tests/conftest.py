import random

import pytest
from fastapi.testclient import TestClient

from tracker.api import app, tracker


@pytest.fixture(scope='session')
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
def nvda_1e6_points(client):
    random.seed(0)

    values_count = 10 ** 6
    values = [random.random() * 10 ** 4 for _ in range(values_count)]

    values_sent = 0
    while values_sent < values_count:
        batch_size = random.randint(9000, 10000)
        client.post(
            '/add_batch', json={
                'symbol': 'NVDA',
                'values': values[values_sent:min(values_sent + batch_size, values_count)]
            }
        )
        values_sent += batch_size


@pytest.fixture
def nvda_expected_stats():
    return {
        1: {
            'min': pytest.approx(128.0595981043786),
            'max': pytest.approx(8421.4346067016),
            'avg': pytest.approx(4522.069022831475),
            'var': pytest.approx(5548730.8684007805),
            'last': pytest.approx(3946.9582187920137)},
        2: {
            'min': pytest.approx(128.0595981043786),
            'max': pytest.approx(9896.52164356374),
            'avg': pytest.approx(4766.153735307077),
            'var': pytest.approx(7276093.494312557),
            'last': pytest.approx(3946.9582187920137)},
        3: {
            'min': pytest.approx(28.052760429577717),
            'max': pytest.approx(9989.009495176113),
            'avg': pytest.approx(4961.698472275404),
            'var': pytest.approx(8550312.610626455),
            'last': pytest.approx(3946.9582187920137)},
        4: {
            'min': pytest.approx(0.061166487218544674),
            'max': pytest.approx(9999.845655419565),
            'avg': pytest.approx(4980.800195881944),
            'var': pytest.approx(8332120.012060966),
            'last': pytest.approx(3946.9582187920137)},
        5: {
            'min': pytest.approx(0.0006078215908367213),
            'max': pytest.approx(9999.972972861955),
            'avg': pytest.approx(4978.878719523702),
            'var': pytest.approx(8360747.8421358215),
            'last': pytest.approx(3946.9582187920137)
        },
        6: {
            'min': pytest.approx(0.0006078215908367213),
            'max': pytest.approx(9999.983960441965),
            'avg': pytest.approx(4996.782627196542),
            'var': pytest.approx(8334203.194891368),
            'last': pytest.approx(3946.9582187920137)
        }
    }
