def test_health(client, api_headers):
    response = client.get(
        "/api/v1/health",
        headers=api_headers
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["model_loaded"] is True