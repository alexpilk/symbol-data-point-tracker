import pytest
from fastapi.testclient import TestClient

from tracker.api import tracker
from tracker.service import Tracker


@pytest.fixture(autouse=True)
def fresh_tracker() -> Tracker:
    tracker.reset()
    return tracker


def test_add_batch(client: TestClient):
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


def test_cannot_add_oversized_batch(client: TestClient):
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


def test_get_stats(nvda_3_points: None, nvda_3_points_expected_stats: dict[str, dict], client: TestClient):
    response = client.get(
        '/stats', params={
            'symbol': 'NVDA',
            'k': 2
        }
    )
    assert response.status_code == 200
    assert response.json() == nvda_3_points_expected_stats


def test_get_stats_for_multiple_symbols(nvda_3_points: None,
                                        nvda_3_points_expected_stats: dict[str, dict],
                                        intl_5_points: None,
                                        intl_5_points_expected_stats: dict[str, dict],
                                        client: TestClient):
    response = client.get(
        '/stats', params={
            'symbol': 'NVDA',
            'k': 2
        }
    )
    assert response.status_code == 200
    assert response.json() == nvda_3_points_expected_stats

    response = client.get(
        '/stats', params={
            'symbol': 'INTL',
            'k': 2
        }
    )
    assert response.status_code == 200
    assert response.json() == intl_5_points_expected_stats


@pytest.mark.parametrize('k', [-1, 0])
def test_get_stats_fails_with_k_too_small(k: int, nvda_3_points: None, client: TestClient):
    response = client.get(
        '/stats', params={
            'symbol': 'NVDA',
            'k': k
        }
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {
                'type': 'greater_than_equal',
                'loc': ['query', 'k'],
                'msg': 'Input should be greater than or equal to 1',
                'input': f'{k}',
                'ctx': {
                    'ge': 1
                }}
        ]
    }


def test_get_stats_fails_with_k_too_large(nvda_3_points: None, client: TestClient):
    k = 9
    response = client.get(
        '/stats', params={
            'symbol': 'NVDA',
            'k': k
        }
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {
                'type': 'less_than_equal',
                'loc': ['query', 'k'],
                'msg': 'Input should be less than or equal to 8',
                'input': f'{k}',
                'ctx': {
                    'le': 8
                }}
        ]
    }


def test_get_stats_uses_last_1ek_data_points(client: TestClient):
    client.post(
        '/add_batch', json={
            'symbol': 'NVDA',
            'values': [1.0] * 5 + [2.0] * 5 + [3.0] * 5 + [4.0] * 5
        }
    )

    response = client.get(
        '/stats', params={
            'symbol': 'NVDA',
            'k': 1
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'min': 3.0,
            'max': 4.0,
            'last': 4.0,
            'avg': 3.5,
            'var': 0.25
        }
    }


def test_get_invalid_symbol(client: TestClient):
    response = client.get(
        '/stats', params={
            'symbol': 'NVDA',
            'k': 2
        }
    )
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {
                'type': 'value_error',
                'loc': ['query', 'symbol'],
                'msg': 'Value error, Symbol "NVDA" does not exist',
                'input': 'NVDA',
                'ctx': {
                    'error': {}
                }
            }
        ]
    }
