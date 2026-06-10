# AI Student Predictor

Predicts a student's final exam marks from study hours, attendance, and previous marks.

**Stack:** SvelteKit (frontend) + Cloudflare Workers (inference API) + Python/sklearn (training)

## Architecture

```
Frontend (SvelteKit)  ──►  Workers API (ONNX)  ──►  Python training pipeline
    :5173                    :8787                      model/train.py
```

- **Frontend** — SvelteKit + Vite, deployed on Cloudflare Pages
- **Inference API** — Cloudflare Workers, ONNX Runtime (WASM) for edge prediction
- **Training** — Python (scikit-learn) trains LinearRegression, exports to ONNX format
- **CI/CD** — GitHub Actions trains model on push, deploys backend + frontend

## Live URLs

| Service | URL |
|---------|-----|
| Frontend | [https://ai-student-predictor.pages.dev](https://ai-student-predictor.pages.dev) |
| API | [https://ai-student-predictor.salmaaaan-kabir.workers.dev](https://ai-student-predictor.salmaaaan-kabir.workers.dev) |

## Run Locally

### Prerequisites

- Node.js 20+
- Python 3.11+
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/) (`npm i -g wrangler`)

### 1. Train the model

```bash
cd model
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python train.py
```

Copies `model.onnx` to `worker/static/model.onnx`.

### 2. Start the Workers API

```bash
cd worker
npm install
npx wrangler dev
```

API runs at `http://127.0.0.1:8787`.

### 3. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://127.0.0.1:5173`.

### Docker (alternative)

```bash
docker compose up
```

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

## Deployment

Push to `main` → GitHub Actions:
1. Trains model (`model/train.py`)
2. Deploys Workers API (`wrangler deploy`)
3. Deploys frontend to Cloudflare Pages

Requires `CLOUDFLARE_API_TOKEN` secret in GitHub repo.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | SvelteKit 5, Vite, TypeScript |
| API | Cloudflare Workers, ONNX Runtime |
| Model | scikit-learn (LinearRegression) |
| Export | ONNX (skl2onnx) |
| CI/CD | GitHub Actions, Wrangler |
