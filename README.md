# AI Student Predictor

A machine learning web application that predicts a student's final exam marks based on their study hours, attendance, and previous exam performance.

Built with FastAPI + scikit-learn + vanilla JS.

## How it works

The backend trains a Linear Regression model on student performance data. Given three inputs — **hours studied per week**, **attendance percentage**, and **previous exam marks** — it predicts the likely final marks.

## Run locally

```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r ../requirements.txt
python3 model.py          # (re)train the model
python3 -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000/app

## API

```
POST /predict
{
  "hours": 7,
  "attendance": 85,
  "previous_marks": 75
}
→ { "predicted_marks": 79.59 }
```

## Tech stack

- **Backend** — FastAPI, scikit-learn, pandas
- **Frontend** — HTML, CSS, JS (no framework)
