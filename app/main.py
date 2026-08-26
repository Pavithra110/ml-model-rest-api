from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import joblib
import uuid
from contextlib import asynccontextmanager
from app.models.schemas import PredictionInput, PredictionOutput

model = None

@asynccontextmanager
async def lifespan(app):
    global model
    model = joblib.load("ml/saved_model/model.joblib")
    print("ML model loaded successfully")
    yield

class PredictionError(Exception):
    pass

app = FastAPI(lifespan=lifespan)

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
def predict(data: PredictionInput):
    request_id = str(uuid.uuid4())

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

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )

    return {
        "prediction": prediction[0],
        "confidence": confidence,
        "request_id": request_id
    }