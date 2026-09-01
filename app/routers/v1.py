import json
import pandas as pd
from fastapi import APIRouter, Request, HTTPException
from app.models.schemas import PredictionInput, PredictionOutput
from app.logging_config import logger
from app.models.schemas import (
    PredictionInput,
    PredictionOutput,
    PredictionBatchInput,
    PredictionBatchOutput
)
from app.config import settings

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

    features = pd.DataFrame([{
        "sepal length (cm)": data.sepal_length,
        "sepal width (cm)": data.sepal_width,
        "petal length (cm)": data.petal_length,
        "petal width (cm)": data.petal_width
    }])

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

@router.post("/predict-batch", response_model=PredictionBatchOutput)
def predict_batch(request: Request, data: PredictionBatchInput):
    request_id = request.state.request_id

    if len(data.inputs) > settings.MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Batch size cannot exceed {settings.MAX_BATCH_SIZE}"
        )

    features = pd.DataFrame([
        {
            "sepal length (cm)": item.sepal_length,
            "sepal width (cm)": item.sepal_width,
            "petal length (cm)": item.petal_length,
            "petal width (cm)": item.petal_width
        }
        for item in data.inputs
    ])

    try:
        model = request.app.state.model

        predictions = model.predict(features)
        probabilities = model.predict_proba(features)

        results = []

        for i in range(len(predictions)):
            confidence = max(probabilities[i])

            results.append({
                "prediction": predictions[i],
                "confidence": confidence,
                "request_id": request_id
            })

        logger.info(
            f"request_id={request_id} batch_size={len(data.inputs)}"
        )

    except Exception as exc:
        logger.error(
            f"request_id={request_id} batch prediction failed error={exc}"
        )
        raise HTTPException(
            status_code=500,
            detail="Batch prediction failed"
        )

    return {
        "predictions": results
    }


@router.get("/model-info")
def model_info():
    with open("ml/saved_model/metadata.json", "r") as file:
        metadata = json.load(file)

    return metadata