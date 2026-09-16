# Testing and Verification

## Phase 4 Integration Testing

The fully containerized API was tested through Docker Compose using real HTTP requests.

### Integration Checklist

| Endpoint | Test | Result |
|---|---|---|
| `/api/v1/health` | Valid API key | Passed |
| `/api/v1/predict` | Valid Iris input + API key | Passed |
| `/api/v1/predict-batch` | Two valid inputs + API key | Passed |
| `/metrics` | Prometheus metrics endpoint | Passed |

### Integration Results

- Docker Compose container started successfully.
- ML model loaded successfully inside the container.
- `/api/v1/health` returned `model_loaded: true`.
- `/api/v1/predict` returned a valid prediction, confidence, and request ID.
- `/api/v1/predict-batch` returned predictions for multiple inputs.
- `/metrics` returned valid Prometheus-format metrics.
- The custom `ml_predictions_total` metric recorded predictions by class.

## Load Testing

A Python `asyncio` and `httpx` load test was used to send 100 concurrent requests to `/api/v1/predict`.

Three valid Iris measurements were distributed across the requests to exercise Setosa, Versicolor, and Virginica predictions.

### Initial Test — Single Uvicorn Worker

| Metric | Result |
|---|---:|
| Total requests | 100 |
| Successful | 100 |
| Failed | 0 |
| Total test duration | 10.4079 seconds |
| Average response time | 10.0340 seconds |
| Fastest response | 7.9844 seconds |
| Slowest response | 10.2927 seconds |

Application logs also showed request durations of approximately 9.7 seconds during the concurrent test.

A separate single-request test completed in approximately 0.115 seconds. This indicated that the model was not inherently slow and that the high latency appeared under concurrent load.

## Performance Fix

The Dockerfile was updated to run Uvicorn with four worker processes instead of one.

### Retest — Four Uvicorn Workers

| Metric | Result |
|---|---:|
| Total requests | 100 |
| Successful | 100 |
| Failed | 0 |
| Total test duration | 5.0493 seconds |
| Average response time | 3.5816 seconds |
| Fastest response | 1.3633 seconds |
| Slowest response | 5.0197 seconds |

The four-worker configuration substantially reduced latency during the 100-request concurrent test while maintaining 100% request success.

## Integration Bug Found and Fixed

During the initial Docker Compose integration test, the container failed to start because the `prometheus-fastapi-instrumentator` package was installed in the local virtual environment but was missing from `requirements.txt`.

### Fix

Added the required dependency to `requirements.txt`:

`prometheus-fastapi-instrumentator==8.1.0`

The Docker image was rebuilt successfully and the container started normally with the ML model and Prometheus instrumentation.

## Monitoring Verification

The `/metrics` endpoint was checked after integration and load testing.

The custom ML metric recorded predictions by class:

- Setosa: 35
- Versicolor: 33
- Virginica: 33

The HTTP metrics also recorded successful `/api/v1/predict` requests and request-duration data.

## Conclusion

The containerized ML API was tested through real HTTP requests, including health, prediction, batch prediction, and Prometheus monitoring.

A 100-request concurrent load test was completed successfully. High latency observed with a single Uvicorn worker was investigated using application logs, container resource usage, and Prometheus metrics. Increasing the number of Uvicorn workers to four reduced the measured average response time from approximately 10.03 seconds to 3.58 seconds, with all 100 requests succeeding.