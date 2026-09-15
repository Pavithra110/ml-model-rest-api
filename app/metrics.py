from prometheus_client import Counter


prediction_counter = Counter(
    "ml_predictions_total",
    "Total number of successful ML predictions by predicted class.",
    ["class"]
)