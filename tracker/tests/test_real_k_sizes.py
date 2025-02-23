def test_get_stats_for_k(nvda_1e8_points, nvda_1e7_points_expected_stats, client):
    response = client.get(
        '/stats', params={
            'symbol': 'NVDA',
            'k': 7
        }
    )
    assert response.status_code == 200
    assert response.json() == nvda_1e7_points_expected_stats
