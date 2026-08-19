import joblib
import pandas as pd

model = joblib.load("ml/saved_model/model.joblib")

sample = pd.DataFrame([{
    "sepal length (cm)": 5.1,
    "sepal width (cm)": 3.5,
    "petal length (cm)": 1.4,
    "petal width (cm)": 0.2
}])

prediction = model.predict(sample)

print("Prediction:", prediction[0])