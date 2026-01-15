# Customer Churn Prediction System ⚡

An end-to-end Machine Learning system that predicts customer churn using a futuristic, responsive web dashboard.

## 🚀 Quick Start (Docker)

The easiest way to run the project is using Docker. Ensure you have Docker Desktop installed.

1.  **Build and Start Containers**:
    ```bash
    docker-compose up --build
    ```
2.  **Access the UI**:
    Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🛠️ Local Development (Standard)

If you prefer to run it without Docker:

1.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the API & UI**:
    ```bash
    uvicorn src.app:app --reload --port 8000
    ```
4.  **Access the UI**:
    Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 📂 Project Structure

- `data/`: Raw dataset and processed data.
- `src/`: Core logic.
  - `eda.py`: Exploratory Data Analysis script.
  - `preprocessing.py`: Data cleaning and feature engineering pipeline.
  - `train.py`: Model training and selection.
  - `app.py`: FastAPI backend.
  - `ui/`: Dashboard (HTML/CSS/JS).
- `models/`: Trained model binaries (`.joblib`).
- `plots/`: Visualizations from EDA.

## 🧪 Testing the API

You can send a POST request to `/predict` with customer data to get a churn prediction. Example payload:

```json
{
  "gender": "Male",
  "SeniorCitizen": 0,
  "Partner": "No",
  "tenure": 12,
  "MonthlyCharges": 70.0,
  "TotalCharges": 840.0,
  "Contract": "Month-to-month",
  "PaymentMethod": "Electronic check",
  ...
}
```

## ✨ Design

The UI features a **Glassmorphism** aesthetic with dynamic background blobs and real-time risk probability visualization.
