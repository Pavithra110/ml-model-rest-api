# ML Model Deployment as a Monitored REST API
REST API for serving a machine learning model using FastAPI

## Project Overview
This project aims to deploy a machine learning model as a REST API. The API will allow a client to send input data to the trained machine learning model and receive a prediction as a response.

## Dataset
The project will use the Iris dataset provided by scikit-learn.

## ML Problem
The goal is to classify an iris flower into one of three species: Setosa, Versicolor, or Virginica, based on its sepal and petal measurements.

## API Contract
The `/predict` endpoint will accept four numerical measurements of an iris flower: sepal length, sepal width, petal length, and petal width. The API will validate the input and pass the valid data to the trained machine learning model. The model will predict the iris flower species, and the API will return the predicted species as the response.

## Request Flow
The client sends four iris flower measurements to the `/predict` endpoint. The API validates the input and, if it is valid, passes the data to the trained machine learning model. The model predicts the iris species, and the API returns the prediction to the client.

### Flow
Client
↓
Request (`/predict`)
↓
Input Validation
↓
ML Model
↓
Prediction
↓
Response
↓
Client
