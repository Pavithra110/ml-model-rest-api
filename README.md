# ML Model Deployment as a Monitored REST API

A machine learning REST API built with FastAPI for predicting Iris flower species. The project includes input validation, API key authentication, API versioning, logging, Prometheus monitoring, Docker packaging, Docker Compose, integration testing, and load testing.

## Project Overview

The application serves a trained Random Forest classification model through a REST API.

A client sends four measurements of an Iris flower:

- Sepal length
- Sepal width
- Petal length
- Petal width

The API validates the input, sends it to the trained ML model, and returns the predicted species and confidence.

The possible predictions are:

- Setosa
- Versicolor
- Virginica

## Dataset

The project uses the Iris dataset provided by scikit-learn.

The model was trained using four features:

- sepal length (cm)
- sepal width (cm)
- petal length (cm)
- petal width (cm)

The trained Random Forest model is saved in:

`ml/saved_model/model.joblib`

Model metadata is stored in:

`ml/saved_model/metadata.json`

## Technologies Used

- Python
- FastAPI
- Uvicorn
- scikit-learn
- pandas
- joblib
- Pydantic
- Pydantic Settings
- Prometheus
- Docker
- Docker Compose
- pytest
- httpx
- GitHub Actions

## Architecture

The overall request flow is:

```text
Client
  |
  v
FastAPI
  |
  v
API Key Authentication
  |
  v
Input Validation
  |
  v
Feature Preparation
  |
  v
Random Forest ML Model
  |
  v
Prediction + Confidence
  |
  v
Logging + Prometheus Metrics
  |
  v
JSON Response


```

## Project Structure

```text
ml-api-project/
├── app/
│   ├── config.py
│   ├── logging_config.py
│   ├── main.py
│   ├── security.py
│   ├── metrics.py
│   ├── models/
│   │   └── schemas.py
│   └── routers/
│       ├── v1.py
│       └── v2.py
├── ml/
│   └── saved_model/
│       ├── model.joblib
│       └── metadata.json
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_model_info.py
│   ├── test_predict.py
│   ├── test_validation.py
│   ├── test_versioning.py
│   └── test_security.py
├── .env.example
├── .gitignore
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── TESTING.md
└── load_test.py
```

## Configuration

The application reads configuration values from environment variables.

For local development, create a `.env` file using `.env.example` as a reference.

Example:

```env
MODEL_PATH=ml/saved_model/model.joblib
LOG_LEVEL=INFO
MAX_BATCH_SIZE=100
API_TITLE=ML Model API
API_KEY=your-secret-api-key
CORS_ORIGINS=http://localhost:3000
```

The `.env` file contains local configuration and secrets. It is excluded from Git and should not be committed.

### API Key Authentication

The versioned API endpoints require an API key.

The API key must be sent using the `X-API-Key` request header.

Example:

```text
X-API-Key: your-secret-api-key
```

Requests with a missing or invalid API key receive HTTP `401 Unauthorized`.

## Running with Docker Compose

Make sure Docker Desktop is running.

Build and start the application:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

To stop the application:

```bash
docker compose down
```

Docker Compose mounts the saved model directory into the container:

```text
./ml/saved_model:/app/ml/saved_model
```

The API runs with four Uvicorn workers inside the container.

## Deployment

The API is deployed online using Render with Docker.

### Live API

https://ml-model-rest-api.onrender.com

### Swagger API Documentation

https://ml-model-rest-api.onrender.com/docs

The deployed API provides the same versioned endpoints as the local Docker Compose environment.

The root endpoint can be accessed without authentication:

```text
https://ml-model-rest-api.onrender.com/

```

## API Endpoints

### 1. Root

**GET**

```text
/
```

Checks whether the API is running.

Example response:

```json
{
  "message": "ML API is alive"
}
```

This endpoint does not require an API key.

### 2. Health Check

**GET**

```text
/api/v1/health
```

Requires an API key.

Example:

```bash
curl -H "X-API-Key: your-secret-api-key" http://localhost:8000/api/v1/health
```

Example response:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

### 3. Single Prediction - API v1

**POST**

```text
/api/v1/predict
```

Requires an API key.

Example request:

```bash
curl -X POST "http://localhost:8000/api/v1/predict" ^
  -H "Content-Type: application/json" ^
  -H "X-API-Key: your-secret-api-key" ^
  -d "{\"sepal_length\":5.1,\"sepal_width\":3.5,\"petal_length\":1.4,\"petal_width\":0.2}"
```

Example response:

```json
{
  "prediction": "setosa",
  "confidence": 1.0,
  "request_id": "example-request-id"
}
```

The response contains:

- `prediction` - predicted Iris species
- `confidence` - highest predicted class probability
- `request_id` - unique ID used for request tracking and logging

### 4. Batch Prediction

**POST**

```text
/api/v1/predict-batch
```

Requires an API key.

The endpoint accepts multiple Iris inputs in a single request.

Example request:

```json
{
  "inputs": [
    {
      "sepal_length": 5.1,
      "sepal_width": 3.5,
      "petal_length": 1.4,
      "petal_width": 0.2
    },
    {
      "sepal_length": 6.0,
      "sepal_width": 2.9,
      "petal_length": 4.5,
      "petal_width": 1.5
    }
  ]
}
```

The maximum batch size is controlled by:

```env
MAX_BATCH_SIZE=100
```

If the configured limit is exceeded, the API returns HTTP `400 Bad Request`.

### 5. Model Information

**GET**

```text
/api/v1/model-info
```

Requires an API key.

Returns metadata about the deployed model.

Example response:

```json
{
  "model_type": "RandomForestClassifier",
  "version": "1.0",
  "training_date": "2026-08-19",
  "expected_features": [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width"
  ]
}
```

### 6. Prediction - API v2

**POST**

```text
/api/v2/predict
```

Requires an API key.

API v2 provides the full probability distribution instead of only the highest confidence value.

Example response:

```json
{
  "prediction": "setosa",
  "probabilities": {
    "setosa": 1.0,
    "versicolor": 0.0,
    "virginica": 0.0
  },
  "request_id": "example-request-id"
}
```

API versioning allows the response contract to change while keeping the existing v1 contract available.

### 7. Prometheus Metrics

**GET**

```text
/metrics
```

Returns Prometheus-compatible monitoring metrics.

The endpoint includes FastAPI HTTP metrics and the custom ML prediction counter:

```text
ml_predictions_total
```

The custom metric tracks successful predictions by predicted class.

## Input Validation

The API validates prediction inputs using Pydantic.

The following validation rules are applied:

- All four measurements are required.
- Values must be numeric.
- Values must be greater than zero.
- Unexpected fields are rejected.
- Invalid requests return HTTP `422 Unprocessable Entity`.

Batch requests are also checked against the configured maximum batch size.

## Error Handling

Prediction failures are handled using a custom prediction error handler.

Instead of exposing an internal traceback to the client, the API returns a controlled HTTP `500` response.

Example:

```json
{
  "detail": "Prediction failed"
}
```

## Logging

The application uses Python logging.

Logs are written to:

```text
logs/app.log
```

The application records information such as:

- HTTP method
- Request path
- Request ID
- Request duration
- Successful requests
- Prediction failures

A rotating file handler is used to prevent the log file from growing indefinitely.

The log file is excluded from Git.

## Monitoring

Prometheus instrumentation is provided using `prometheus-fastapi-instrumentator`.

The application exposes:

```text
/metrics
```

The custom metric:

```text
ml_predictions_total
```

counts successful predictions by predicted class.

This provides a basic monitoring foundation for tracking API traffic and model prediction activity.

## CORS

The API includes CORS configuration.

By default, the allowed frontend origin is:

```text
http://localhost:3000
```

Allowed methods:

- GET
- POST

Allowed request headers include:

- Content-Type
- X-API-Key

CORS origins can be changed through the `CORS_ORIGINS` environment variable.

## Rate Limiting

Rate limiting is not implemented in this MVP.

For a production deployment, a rate limiter or API gateway could restrict the number of requests a client can make within a time window.

A production implementation could use a reverse proxy, API gateway, or a shared Redis-backed rate limiter so that limits work consistently across multiple API instances.

## Testing

The project uses pytest for automated testing.

Run the test suite with:

```bash
pytest -v
```

The tests cover:

- Health endpoint
- Prediction endpoint
- Input validation
- Batch-size validation
- Model information
- API versioning
- API key authentication
- Unexpected input fields

The complete automated test suite currently passes successfully.

## Integration Testing

The API was tested end-to-end using the Docker Compose environment.

The integration checks covered:

- Health endpoint
- Single prediction
- Batch prediction
- Prometheus metrics
- API key authentication

The detailed testing results are documented in `TESTING.md`.

## Load Testing

A custom asynchronous load test is available in:

```text
load_test.py
```

The test sends 100 concurrent prediction requests.

The load test was used to compare API performance with different Uvicorn worker configurations.

With one worker:

- 100 successful requests
- 0 failed requests
- Total time: approximately 10.41 seconds

After changing the container to four Uvicorn workers:

- 100 successful requests
- 0 failed requests
- Total time: approximately 5.05 seconds

These results are from the local Docker test environment and are intended as a basic performance comparison rather than a production benchmark.

## What I Learned

Through this project, I learned how to take a machine learning model and expose it through a REST API.

I learned how FastAPI receives and validates request data before sending it to the model.

I learned how to load a saved machine learning model when the application starts instead of training the model for every request.

I learned how API versioning allows different response formats to exist without breaking existing clients.

I learned how API key authentication, CORS, input validation, and controlled error handling improve API robustness.

I also learned how logging and Prometheus metrics can be used to monitor an API.

Docker and Docker Compose helped me understand how to package the application and run it consistently in a containerized environment.

Testing with pytest and load testing helped me verify both correctness and basic performance.

## Independent Extension

### GitHub Actions CI

The independent extension for this project is a GitHub Actions continuous integration workflow.

The workflow runs the pytest test suite automatically when code is pushed to the GitHub repository.

This helps detect test failures whenever new code is pushed.

The workflow is stored in:

```text
.github/workflows/ci.yml
```

## GitHub Repository

The project repository is:

`https://github.com/Pavithra110/ml-model-rest-api`

## Conclusion

This project demonstrates a complete basic machine learning deployment workflow:

```text
Train Model
    |
    v
Save Model
    |
    v
FastAPI REST API
    |
    v
Input Validation
    |
    v
Authentication
    |
    v
ML Prediction
    |
    v
Logging + Monitoring
    |
    v
Automated Testing
    |
    v
Docker + Docker Compose
    |
    v
Continuous Integration
```

