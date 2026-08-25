from fastapi import FastAPI
import joblib
import uuid
from contextlib import asynccontextmanager
from app.models.schemas import PredictionInput

model = None

@asynccontextmanager
async def lifespan(app):
    global model
    model = joblib.load("ml/saved_model/model.joblib")
    print("ML model loaded successfully")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "ML API is alive"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None
    }

@app.post("/predict")
def predict(data: PredictionInput):
    request_id = str(uuid.uuid4())

    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    prediction = model.predict(features)

    probabilities = model.predict_proba(features)

    confidence = max(probabilities[0])

    return {
        "prediction": prediction[0],
        "confidence": confidence,
        "request_id": request_id
    }