from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(title="Customer Churn Prediction API")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load preprocessor and model
MODEL_PATH = 'models/churn_model.joblib'
PREPROCESSOR_PATH = 'models/preprocessor.joblib'

if os.path.exists(MODEL_PATH) and os.path.exists(PREPROCESSOR_PATH):
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
else:
    model = None
    preprocessor = None

class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float



@app.get("/health")
def health_check():
    if model and preprocessor:
        return {"status": "healthy", "model_loaded": True}
    return {"status": "degraded", "model_loaded": False}

@app.post("/predict")
def predict(data: CustomerData):
    if not model or not preprocessor:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Convert input to DataFrame
    input_df = pd.DataFrame([data.dict()])
    
    # Preprocess
    processed_data = preprocessor.transform(input_df)
    
    # Predict
    prediction = model.predict(processed_data)
    probability = model.predict_proba(processed_data)[:, 1]
    
    return {
        "prediction": "Churn" if prediction[0] == 1 else "No Churn",
        "probability": float(probability[0])
    }

# Serve static files for UI
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ui_path = os.path.join(BASE_DIR, "ui")

if os.path.exists(ui_path):
    app.mount("/", StaticFiles(directory=ui_path, html=True), name="ui")


