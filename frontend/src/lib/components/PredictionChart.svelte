<script lang="ts">
  import { onDestroy } from 'svelte';
  import Chart from 'chart.js/auto';

  let { hours = 5, attendance = 75, previousMarks = 65 } = $props();

  const COEFFICIENTS = [1.4948909, 0.19169791, 0.5830761];
  const INTERCEPT = 7.9676971435546875;

  function predict(h: number, a: number, p: number): number {
    return COEFFICIENTS[0] * h + COEFFICIENTS[1] * a + COEFFICIENTS[2] * p + INTERCEPT;
  }

  type Mode = 'hours' | 'attendance' | 'previous_marks';
  let mode = $state<Mode>('hours');

  let canvas: HTMLCanvasElement;
  let chart: Chart | null = null;

  const MODE_LABELS: Record<Mode, string> = {
    hours: 'Hours Studied (per week)',
    attendance: 'Attendance (%)',
    previous_marks: 'Previous Exam Marks',
  };

  const MODE_RANGES: Record<Mode, { min: number; max: number; step: number }> = {
    hours: { min: 0, max: 24, step: 1 },
    attendance: { min: 0, max: 100, step: 5 },
    previous_marks: { min: 0, max: 100, step: 5 },
  };

  function buildChartData() {
    const range = MODE_RANGES[mode];
    const labels: number[] = [];
    const values: number[] = [];
    for (let v = range.min; v <= range.max; v += range.step) {
      labels.push(Math.round(v * 10) / 10);
      let h = mode === 'hours' ? v : hours;
      let a = mode === 'attendance' ? v : attendance;
      let p = mode === 'previous_marks' ? v : previousMarks;
      values.push(Math.round(predict(h, a, p) * 100) / 100);
    }

    let currentValue = mode === 'hours' ? hours : mode === 'attendance' ? attendance : previousMarks;

    return { labels, values, currentValue };
  }

  function renderChart() {
    const { labels, values, currentValue } = buildChartData();

    if (chart) {
      chart.data.labels = labels;
      chart.data.datasets[0].data = values;
      chart.update('none');
      return;
    }

    chart = new Chart(canvas, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Predicted Marks',
          data: values,
          borderColor: '#818cf8',
          backgroundColor: 'rgba(129, 140, 248, 0.1)',
          fill: true,
          tension: 0.3,
          pointRadius: 3,
          pointHoverRadius: 5,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 0 },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#1e293b',
            titleColor: '#e2e8f0',
            bodyColor: '#94a3b8',
            borderColor: '#334155',
            borderWidth: 1,
          },
        },
        scales: {
          x: {
            title: { display: true, text: MODE_LABELS[mode], color: '#94a3b8' },
            ticks: { color: '#64748b' },
            grid: { color: 'rgba(51, 65, 85, 0.3)' },
          },
          y: {
            title: { display: true, text: 'Predicted Marks', color: '#94a3b8' },
            min: 0,
            max: 100,
            ticks: { color: '#64748b' },
            grid: { color: 'rgba(51, 65, 85, 0.3)' },
          },
        },
      },
    });
  }

  $effect(() => {
    hours; attendance; previousMarks; mode;
    if (canvas) renderChart();
  });

  onDestroy(() => {
    chart?.destroy();
  });
</script>

<div class="chart-section">
  <div class="chart-header">
    <h3>Sensitivity Analysis</h3>
    <div class="mode-tabs">
      {#each Object.entries(MODE_LABELS) as [key, label]}
        <button
          class="mode-tab"
          class:active={mode === key}
          onclick={() => mode = key as Mode}
        >
          {label.split('(')[0].trim()}
        </button>
      {/each}
    </div>
  </div>
  <div class="chart-wrapper">
    <canvas bind:this={canvas}></canvas>
  </div>
</div>

<style>
  .chart-section {
    margin-top: 28px;
    padding: 20px;
    border-radius: 12px;
    background: var(--bg-primary);
    border: 1px solid var(--border);
  }
  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    flex-wrap: wrap;
    gap: 8px;
  }
  .chart-header h3 {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
  }
  .mode-tabs {
    display: flex;
    gap: 4px;
  }
  .mode-tab {
    padding: 4px 12px;
    border: 1px solid var(--border);
    border-radius: 6px;
    background: transparent;
    color: var(--text-secondary);
    font-size: 12px;
    cursor: pointer;
    transition: all 0.15s;
  }
  .mode-tab:hover {
    border-color: var(--accent-start);
    color: var(--text-primary);
  }
  .mode-tab.active {
    background: var(--accent-start);
    border-color: var(--accent-start);
    color: white;
  }
  .chart-wrapper {
    height: 250px;
  }
</style>
