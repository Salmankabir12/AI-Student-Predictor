import { describe, it, expect, vi, beforeEach } from 'vitest';
import { predict, ApiError } from '../api';

const mockFetch = vi.fn();
globalThis.fetch = mockFetch;

describe('predict', () => {
  beforeEach(() => {
    mockFetch.mockReset();
  });

  it('returns predicted marks on success', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ predicted_marks: 85.5 }),
    });

    const result = await predict({ hours: 10, attendance: 90, previous_marks: 80 });
    expect(result.predicted_marks).toBe(85.5);
  });

  it('sends correct request body', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ predicted_marks: 85.5 }),
    });

    await predict({ hours: 10, attendance: 90, previous_marks: 80 });

    expect(mockFetch).toHaveBeenCalledWith('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ hours: 10, attendance: 90, previous_marks: 80 }),
    });
  });

  it('throws ApiError on API error', async () => {
    mockFetch.mockResolvedValue({
      ok: false,
      status: 400,
      json: () => Promise.resolve({ detail: 'hours must be between 0 and 24' }),
    });

    await expect(predict({ hours: 99, attendance: 50, previous_marks: 50 }))
      .rejects
      .toThrow(ApiError);
  });

  it('throws ApiError with default message when no detail', async () => {
    mockFetch.mockResolvedValue({
      ok: false,
      status: 500,
      json: () => Promise.resolve({}),
    });

    await expect(predict({ hours: 5, attendance: 50, previous_marks: 50 }))
      .rejects
      .toThrow('Something went wrong');
  });

  it('throws ApiError with correct status', async () => {
    mockFetch.mockResolvedValue({
      ok: false,
      status: 422,
      json: () => Promise.resolve({ detail: 'Validation error' }),
    });

    try {
      await predict({ hours: 5, attendance: 50, previous_marks: 50 });
    } catch (e) {
      expect(e).toBeInstanceOf(ApiError);
      expect((e as ApiError).status).toBe(422);
    }
  });

  it('handles network errors', async () => {
    mockFetch.mockRejectedValue(new TypeError('Failed to fetch'));

    await expect(predict({ hours: 5, attendance: 50, previous_marks: 50 }))
      .rejects
      .toThrow(TypeError);
  });
});
