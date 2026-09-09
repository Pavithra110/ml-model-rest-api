def test_v1_and_v2_response_shapes(client, api_headers):

    input_data = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    v1_response = client.post(
        "/api/v1/predict",
        headers=api_headers,
        json=input_data
    )

    v2_response = client.post(
        "/api/v2/predict",
        headers=api_headers,
        json=input_data
    )

    assert v1_response.status_code == 200
    assert v2_response.status_code == 200

    v1_data = v1_response.json()
    v2_data = v2_response.json()

    # v1 keeps its original response shape
    assert set(v1_data.keys()) == {
        "prediction",
        "confidence",
        "request_id"
    }

    # v2 has the new response shape
    assert set(v2_data.keys()) == {
        "prediction",
        "probabilities",
        "request_id"
    }

    # Prove the breaking change
    assert "confidence" not in v2_data
    assert "probabilities" not in v1_data

    # Check that v2 contains probabilities for all classes
    assert set(v2_data["probabilities"].keys()) == {
        "setosa",
        "versicolor",
        "virginica"
    }