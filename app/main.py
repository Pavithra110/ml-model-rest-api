from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import joblib
import uuid
from contextlib import asynccontextmanager
from app.models.schemas import PredictionInput, PredictionOutput
from app.logging_config import logger
import time

model = None

@asynccontextmanager
async def lifespan(app):
    global model
    model = joblib.load("ml/saved_model/model.joblib")
    logger.info("ML model loaded successfully")
    yield

class PredictionError(Exception):
    pass

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def log_requests(request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
    f"request_id={request_id} method={request.method} "
    f"path={request.url.path} duration={duration:.4f}s"
    )

    return response

@app.exception_handler(PredictionError)
async def prediction_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Prediction error"}
    )

@app.get("/")
def root():
    return {"message": "ML API is alive"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=PredictionOutput)
def predict(request: Request, data: PredictionInput):
    request_id = request.state.request_id

    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    try:
        prediction = model.predict(features)
        probabilities = model.predict_proba(features)
        confidence = max(probabilities[0])

        logger.info(
            f"request_id={request_id} prediction={prediction[0]}"
        )

    except Exception as exc:
        logger.error(
            f"request_id={request_id} prediction failed error={exc}"
        )
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )

    return {
        "prediction": prediction[0],
        "confidence": confidence,
        "request_id": request_id
    }