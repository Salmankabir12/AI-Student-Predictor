const COEFFICIENTS = [1.4948909, 0.19169791, 0.5830761];
const INTERCEPT = 7.9676971435546875;

interface PredictRequest {
  hours: number;
  attendance: number;
  previous_marks: number;
}

interface PredictResponse {
  predicted_marks: number;
}

interface ErrorResponse {
  detail: string;
}

const ALLOWED_ORIGINS = ['*'];

function corsHeaders(origin: string): Record<string, string> {
  return {
    'Access-Control-Allow-Origin': ALLOWED_ORIGINS.includes('*') ? '*' : origin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

function validateInput(data: PredictRequest): string | null {
  if (typeof data.hours !== 'number' || data.hours < 0 || data.hours > 24) {
    return 'hours must be a number between 0 and 24';
  }
  if (typeof data.attendance !== 'number' || data.attendance < 0 || data.attendance > 100) {
    return 'attendance must be a number between 0 and 100';
  }
  if (typeof data.previous_marks !== 'number' || data.previous_marks < 0 || data.previous_marks > 100) {
    return 'previous_marks must be a number between 0 and 100';
  }
  return null;
}

function predict(hours: number, attendance: number, previous_marks: number): number {
  const raw = COEFFICIENTS[0] * hours
    + COEFFICIENTS[1] * attendance
    + COEFFICIENTS[2] * previous_marks
    + INTERCEPT;
  return Math.round(raw * 100) / 100;
}

export default {
  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin') || '*';
    const headers = { 'Content-Type': 'application/json', ...corsHeaders(origin) };

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers });
    }

    if (request.method === 'GET' && url.pathname === '/') {
      return new Response(
        JSON.stringify({ status: 'ok', service: 'AI Student Predictor' }),
        { headers },
      );
    }

    if (request.method === 'POST' && url.pathname === '/predict') {
      try {
        const data: PredictRequest = await request.json();

        const validationError = validateInput(data);
        if (validationError) {
          return new Response(
            JSON.stringify({ detail: validationError } satisfies ErrorResponse),
            { status: 400, headers },
          );
        }

        const predicted = predict(data.hours, data.attendance, data.previous_marks);

        return new Response(
          JSON.stringify({ predicted_marks: predicted } satisfies PredictResponse),
          { headers },
        );
      } catch (err) {
        console.error('Prediction error:', err);
        return new Response(
          JSON.stringify({ detail: 'Internal server error during prediction' } satisfies ErrorResponse),
          { status: 500, headers },
        );
      }
    }

    return new Response(JSON.stringify({ detail: 'Not found' }), { status: 404, headers });
  },
} satisfies ExportedHandler;
