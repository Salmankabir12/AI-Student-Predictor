from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import pickle
import numpy as np
import pandas as pd
import os

app = FastAPI(title="AI Student Predictor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

class PredictRequest(BaseModel):
    hours: float = Field(..., ge=0, le=24, description="Hours studied per week")
    attendance: float = Field(..., ge=0, le=100, description="Attendance percentage")
    previous_marks: float = Field(..., ge=0, le=100, description="Previous exam marks")

class PredictResponse(BaseModel):
    predicted_marks: float

@app.get("/")
def home():
    return {"message": "AI Student Predictor API", "endpoint": "POST /predict"}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        input_data = pd.DataFrame([[req.hours, req.attendance, req.previous_marks]],
                                    columns=['hours', 'attendance', 'previous_marks'])
        prediction = model.predict(input_data)
        predicted = round(float(prediction[0]), 2)
        return PredictResponse(predicted_marks=predicted)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
os.makedirs(frontend_path, exist_ok=True)
app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="frontend")
