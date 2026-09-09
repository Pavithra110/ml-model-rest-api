def test_predict(client, api_headers):

    response = client.post(
        "/api/v1/predict",
        headers=api_headers,
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
    )

    assert response.status_code == 200
    assert response.json()["prediction"] in ["setosa", "versicolor", "virginica"]