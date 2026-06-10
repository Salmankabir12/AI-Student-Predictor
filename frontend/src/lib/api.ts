export interface PredictRequest {
  hours: number;
  attendance: number;
  previous_marks: number;
}

export interface PredictResponse {
  predicted_marks: number;
}

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

const API_BASE = import.meta.env.PROD
  ? 'https://ai-student-predictor.salmaaaan-kabir.workers.dev'
  : '';

export async function predict(data: PredictRequest): Promise<PredictResponse> {
  const res = await fetch(`${API_BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  const body = await res.json();

  if (!res.ok) {
    throw new ApiError(res.status, body.detail || 'Something went wrong');
  }

  return body as PredictResponse;
}
