def test_model_info(client):

    response = client.get("/api/v1/model-info")

    assert response.status_code == 200
    assert "model_type" in response.json()
    assert "version" in response.json()
    assert "training_date" in response.json()
    assert "expected_features" in response.json()