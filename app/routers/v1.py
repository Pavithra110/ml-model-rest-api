from fastapi import APIRouter, Request, HTTPException
from app.models.schemas import PredictionInput, PredictionOutput
from app.logging_config import logger

router = APIRouter(prefix="/api/v1")

@router.get("/health")
def health(request: Request):
    return {
        "status": "ok",
        "model_loaded": request.app.state.model is not None
    }

@router.post("/predict", response_model=PredictionOutput)
def predict(request: Request, data: PredictionInput):
    request_id = request.state.request_id

    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    try:
        model = request.app.state.model

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

# API v2 can use a separate response schema if additional fields are needed,
# while keeping the v1 response unchanged for existing clients.