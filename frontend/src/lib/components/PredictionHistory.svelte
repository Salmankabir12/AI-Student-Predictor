<script lang="ts">
  import { history, clearHistory, type HistoryEntry } from '$lib/stores/history';

  let isOpen = $state(false);

  function formatDate(ts: number): string {
    return new Date(ts).toLocaleString();
  }
</script>

<div class="history-section">
  <button class="toggle-btn" onclick={() => isOpen = !isOpen}>
    <span>Prediction History ({$history.length})</span>
    <span class="chevron" class:open={isOpen}>▼</span>
  </button>

  {#if isOpen}
    <div class="history-content">
      {#if $history.length === 0}
        <p class="empty">No predictions yet.</p>
      {:else}
        <div class="history-actions">
          <button class="clear-btn" onclick={clearHistory}>Clear All</button>
        </div>
        <div class="history-list">
          {#each $history as entry (entry.id)}
            <div class="history-item">
              <div class="item-header">
                <span class="item-marks">{entry.predicted_marks}</span>
                <span class="item-time">{formatDate(entry.timestamp)}</span>
              </div>
              <div class="item-details">
                Hours: {entry.hours} · Attendance: {entry.attendance}% · Previous: {entry.previous_marks}
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .history-section {
    margin-top: 16px;
  }
  .toggle-btn {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border: 1px solid var(--border);
    border-radius: 10px;
    background: var(--bg-card);
    color: var(--text-primary);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: border-color 0.15s;
  }
  .toggle-btn:hover {
    border-color: var(--accent-start);
  }
  .chevron {
    transition: transform 0.2s;
    font-size: 10px;
    color: var(--text-muted);
  }
  .chevron.open {
    transform: rotate(180deg);
  }
  .history-content {
    margin-top: 8px;
    padding: 16px;
    border-radius: 10px;
    background: var(--bg-primary);
    border: 1px solid var(--border);
  }
  .empty {
    color: var(--text-muted);
    font-size: 13px;
    text-align: center;
    padding: 20px;
  }
  .history-actions {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 8px;
  }
  .clear-btn {
    padding: 4px 10px;
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 6px;
    background: transparent;
    color: var(--error-text);
    font-size: 11px;
    cursor: pointer;
    transition: background 0.15s;
  }
  .clear-btn:hover {
    background: var(--error-bg);
  }
  .history-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
    max-height: 300px;
    overflow-y: auto;
  }
  .history-item {
    padding: 10px 12px;
    border-radius: 8px;
    background: var(--bg-card);
    border: 1px solid var(--border);
  }
  .item-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
  }
  .item-marks {
    font-size: 18px;
    font-weight: 700;
    background: var(--gradient-text);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .item-time {
    font-size: 11px;
    color: var(--text-muted);
  }
  .item-details {
    font-size: 12px;
    color: var(--text-secondary);
  }
</style>
