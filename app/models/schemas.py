from pydantic import BaseModel, ConfigDict, Field
from typing import List


class PredictionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sepal_length: float = Field(..., gt=0)
    sepal_width: float = Field(..., gt=0)
    petal_length: float = Field(..., gt=0)
    petal_width: float = Field(..., gt=0)


class PredictionOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prediction: str
    confidence: float
    request_id: str


class PredictionV2Output(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prediction: str
    probabilities: dict[str, float]
    request_id: str


class PredictionBatchInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    inputs: List[PredictionInput]


class PredictionBatchOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    predictions: List[PredictionOutput]