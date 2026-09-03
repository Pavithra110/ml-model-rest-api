import pandas as pd
from fastapi import APIRouter, Request

from app.models.schemas import PredictionInput, PredictionV2Output


router = APIRouter(prefix="/api/v2")


@router.post("/predict", response_model=PredictionV2Output)
def predict(request: Request, data: PredictionInput):

    request_id = request.state.request_id

    features = pd.DataFrame([{
        "sepal length (cm)": data.sepal_length,
        "sepal width (cm)": data.sepal_width,
        "petal length (cm)": data.petal_length,
        "petal width (cm)": data.petal_width
    }])

    model = request.app.state.model

    prediction = model.predict(features)[0]

    probabilities = model.predict_proba(features)[0]

    classes = model.classes_

    probability_dict = dict(zip(classes, probabilities))

    return {
        "prediction": prediction,
        "probabilities": probability_dict,
        "request_id": request_id
    }