<script lang="ts">
  import { predict, ApiError, type PredictRequest } from '$lib/api';
  import PredictionChart from '$lib/components/PredictionChart.svelte';
  import PredictionHistory from '$lib/components/PredictionHistory.svelte';
  import { addEntry } from '$lib/stores/history';

  let hours = 5;
  let attendance = 75;
  let previousMarks = 65;
  let loading = false;
  let result: number | null = null;
  let error: string | null = null;

  async function handleSubmit(e: Event) {
    e.preventDefault();
    loading = true;
    error = null;
    result = null;

    try {
      const data: PredictRequest = {
        hours,
        attendance,
        previous_marks: previousMarks,
      };
      const res = await predict(data);
      result = res.predicted_marks;
      addEntry({
        hours: data.hours,
        attendance: data.attendance,
        previous_marks: data.previous_marks,
        predicted_marks: res.predicted_marks,
      });
    } catch (err) {
      if (err instanceof ApiError) {
        error = err.message;
      } else {
        error = 'Network error. Make sure the server is running.';
      }
    } finally {
      loading = false;
    }
  }
</script>

<div class="card">
  <h1>AI Student Predictor</h1>
  <p class="subtitle">Predict final exam marks based on study habits</p>
  <p class="deployment-badge">v1.0.0 · Cloudflare Workers + SvelteKit</p>

  <form onsubmit={handleSubmit}>
    <div class="form-group">
      <label for="hours">Hours Studied (per week)</label>
      <input id="hours" type="number" bind:value={hours} min="0" max="24" step="0.5" required />
      <div class="input-hint">Range: 0 – 24 hours</div>
    </div>

    <div class="form-group">
      <label for="attendance">Attendance (%)</label>
      <input id="attendance" type="number" bind:value={attendance} min="0" max="100" step="1" required />
      <div class="input-hint">Range: 0 – 100%</div>
    </div>

    <div class="form-group">
      <label for="previous_marks">Previous Exam Marks</label>
      <input id="previous_marks" type="number" bind:value={previousMarks} min="0" max="100" step="0.5" required />
      <div class="input-hint">Range: 0 – 100</div>
    </div>

    <button type="submit" disabled={loading}>
      {#if loading}
        Predicting...
      {:else}
        Predict Marks
      {/if}
    </button>
  </form>

  {#if result !== null}
    <div class="result">
      <div class="result-label">Predicted Final Marks</div>
      <div class="result-value">{result.toFixed(1)}</div>
      <div class="result-note">Based on the regression model trained on student performance data.</div>
    </div>
  {/if}

  {#if error}
    <div class="error">{error}</div>
  {/if}

  <PredictionChart {hours} {attendance} previousMarks={previousMarks} />
  <PredictionHistory />
</div>

<style>
  .card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 40px;
    max-width: 500px;
    width: 100%;
    box-shadow: 0 25px 50px rgba(0,0,0,0.3);
  }
  h1 {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 4px;
    background: var(--gradient-text);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .subtitle {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 28px;
  }
  .form-group { margin-bottom: 20px; }
  label {
    display: block;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 6px;
    color: #cbd5e1;
  }
  input {
    width: 100%;
    padding: 12px 14px;
    border: 1px solid var(--border);
    border-radius: 10px;
    background: var(--bg-primary);
    color: var(--text-primary);
    font-size: 15px;
    transition: border-color 0.2s;
  }
  input:focus {
    outline: none;
    border-color: var(--accent-start);
  }
  .input-hint {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 4px;
  }
  button {
    width: 100%;
    padding: 14px;
    border: none;
    border-radius: 10px;
    background: linear-gradient(135deg, var(--accent-start), var(--accent-end));
    color: white;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.2s, transform 0.1s;
  }
  button:hover:not(:disabled) { opacity: 0.9; }
  button:active:not(:disabled) { transform: scale(0.98); }
  button:disabled { opacity: 0.5; cursor: not-allowed; }
  .result {
    margin-top: 24px;
    padding: 20px;
    border-radius: 12px;
    background: var(--bg-primary);
    border: 1px solid var(--border);
  }
  .result-label { font-size: 13px; color: var(--text-secondary); margin-bottom: 4px; }
  .result-value {
    font-size: 36px;
    font-weight: 700;
    background: var(--gradient-text);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .result-note { font-size: 13px; color: var(--text-muted); margin-top: 8px; }
  .deployment-badge {
    font-size: 11px;
    color: var(--text-muted);
    margin-bottom: 24px;
    letter-spacing: 0.5px;
  }
  .error {
    margin-top: 16px;
    padding: 12px;
    border-radius: 8px;
    background: var(--error-bg);
    border: 1px solid var(--error-border);
    color: var(--error-text);
    font-size: 14px;
  }
</style>
