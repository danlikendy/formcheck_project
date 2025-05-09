import os
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Загружаем модель с абсолютным путём для Docker

model_path = '/app/models/rf_model.pkl'
model = joblib.load(model_path)

class PlayerData(BaseModel):
    injury: int
    recovery_days: int
    rating_before_clean: float
    age: int
    position: int

@app.post("/predict")
def predict(data: PlayerData):
    X_input = pd.DataFrame([[data.injury, data.recovery_days, data.rating_before_clean, data.age, data.position]],
                           columns=['injury', 'recovery_days', 'rating_before_clean', 'age', 'position'])

    prediction = model.predict(X_input)[0]
    probability = model.predict_proba(X_input)[0][1]

    return {
        "risk_prediction": int(prediction),
        "risk_probability": round(probability * 100, 2),
        "recommendation": "Снизить нагрузку и увеличить восстановление" if prediction == 1 else "Можно продолжать текущую программу"
    }