import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize('k', range(1, 7))
def test_get_stats_for_k(k: int, nvda_1e6_points: None, nvda_expected_stats: dict[int, dict], client: TestClient):
    response = client.get(
        '/stats', params={
            'symbol': 'NVDA',
            'k': k
        }
    )
    assert response.status_code == 200
    assert response.json() == {'data': nvda_expected_stats[k]}
