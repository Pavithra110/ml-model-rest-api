def test_missing_api_key(client):
    response = client.post(
        "/api/v1/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
    )

    assert response.status_code == 401


def test_invalid_api_key(client):
    response = client.post(
        "/api/v1/predict",
        headers={
            "X-API-Key": "wrong-key"
        },
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
    )

    assert response.status_code == 401


def test_unexpected_extra_field(client, api_headers):
    response = client.post(
        "/api/v1/predict",
        headers=api_headers,
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
            "extra_field": "not allowed"
        }
    )

    assert response.status_code == 422