# AI Student Predictor — AGENTS.md

## Stack

| Layer | Tech |
|---|---|
| Frontend | **SvelteKit 2** + Svelte 5 + Vite 6 |
| API | **Cloudflare Workers** (TypeScript, wrangler 4.x) |
| Charts | chart.js 4.5.1 |
| Training | Python 3.11+ / scikit-learn / ONNX export |
| CI/CD | GitHub Actions (`wrangler-action` v3) |
| Testing | Vitest (frontend), pytest (Python model) |
| Deploy | Cloudflare Pages (frontend) + Workers (API) |

## Commands

```bash
# Frontend (http://localhost:5173)
cd frontend && npm install && npm run dev

# Workers API (http://127.0.0.1:8787)
cd worker && npm install && npx wrangler dev

# Docker (both at once)
docker compose up

# Model training
cd model && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && python train.py

# Frontend tests
cd frontend && npm test        # vitest run
npm run test:watch             # vitest watch

# Model tests
cd model && python -m pytest tests/ -v

# Worker typecheck
cd worker && npx tsc --noEmit
```

## Architecture

```
SvelteKit frontend → POST /predict → Cloudflare Worker → hardcoded coefficients → prediction
```

**Key quirk: Worker uses hardcoded coefficients, not ONNX runtime.** The `model.onnx` exists in `worker/static/` but is never loaded by `src/index.ts`. Coefficients were extracted from scikit-learn `LinearRegression` and hardcoded.

## API

`POST /predict` with JSON body `{hours, attendance, previous_marks}`. Each validated 0-24, 0-100, 0-100. Returns `{predicted_marks: number}`.

Live: `https://ai-student-predictor.salmaaaan-kabir.workers.dev`

## Frontend quirks

- **Signup page is cosmetic** — form data goes nowhere, just shows "Account created! (demo)"
- **Dev proxy** — Vite proxies `/predict` → `http://127.0.0.1:8787`
- **Prediction history** persists to `localStorage` (key `prediction_history`, max 100)
- **Chart duplicates coefficients** client-side for sensitivity analysis

## CI/CD (`.github/workflows/train-deploy.yml`)

Triggers on push to `main` with changes to `model/**`, `worker/**`, `frontend/**`, `.github/workflows/**`.

3 parallel jobs:
1. `train` — Python training pipeline
2. `deploy-worker` — `wrangler-action` deploy
3. `deploy-frontend` — build + `wrangler pages deploy`

**CI quirk:** `train` job doesn't upload ONNX as artifact, so deploy jobs don't get the freshly trained model. The committed `.onnx` is what deploys.

## Env vars

| Var | Where used |
|---|---|
| `CLOUDFLARE_API_TOKEN` | GitHub Actions secret only |
| `API_BASE` | Frontend, set via `import.meta.env.PROD` (empty in dev → proxy, live URL in prod) |

No `.env` files exist. No `.dev.vars`.

## Remnants

- `backend/` is dead (legacy FastAPI, archived to `archive/`)
- Two datasets: `model/student_data.csv` (200 rows, active) and `backend/student_data.csv` (10 rows, stale)
- `wrangler.toml` compatibility date is `2025-07-18` (stale/future)
