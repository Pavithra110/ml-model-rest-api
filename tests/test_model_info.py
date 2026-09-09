def test_model_info(client, api_headers):

    response = client.get(
        "/api/v1/model-info",
        headers=api_headers
    )

    assert response.status_code == 200
    assert "model_type" in response.json()
    assert "version" in response.json()
    assert "training_date" in response.json()
    assert "expected_features" in response.json()