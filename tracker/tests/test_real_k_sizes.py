import pytest


@pytest.mark.parametrize('k', range(1, 7))
def test_get_stats_for_k(k, nvda_1e6_points, nvda_expected_stats, client):
    response = client.get(
        '/stats', params={
            'symbol': 'NVDA',
            'k': k
        }
    )
    assert response.status_code == 200
    assert response.json() == {'data': nvda_expected_stats[k]}
