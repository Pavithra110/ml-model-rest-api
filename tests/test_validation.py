def test_predict_missing_field(client, api_headers):

    response = client.post(
        "/api/v1/predict",
        headers=api_headers,
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_width": 0.2
        }
    )

    assert response.status_code == 422


def test_predict_invalid_type(client, api_headers):

    response = client.post(
        "/api/v1/predict",
        headers=api_headers,
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": "hello",
            "petal_width": 0.2
        }
    )

    assert response.status_code == 422


def test_predict_batch_too_large(client, api_headers):

    valid_input = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    response = client.post(
        "/api/v1/predict-batch",
        headers=api_headers,
        json={
            "inputs": [valid_input] * 101
        }
    )

    assert response.status_code == 400