from fastapi import FastAPI
import joblib
from contextlib import asynccontextmanager

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

@app.post("/predict")
def predict():
    data = {
        "sepal_length": 6.7,
        "sepal_width": 3.1,
        "petal_length": 4.7,
        "petal_width": 1.5
    }

    features = [[
        data["sepal_length"],
        data["sepal_width"],
        data["petal_length"],
        data["petal_width"]
    ]]

    prediction = model.predict(features)

    return {"prediction": prediction[0]}