import { writable } from 'svelte/store';

export interface HistoryEntry {
  id: string;
  timestamp: number;
  hours: number;
  attendance: number;
  previous_marks: number;
  predicted_marks: number;
}

const STORAGE_KEY = 'prediction_history';
const MAX_ENTRIES = 100;

function loadHistory(): HistoryEntry[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveHistory(entries: HistoryEntry[]): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
  } catch {
    // storage full or unavailable
  }
}

const initial = loadHistory();
export const history = writable<HistoryEntry[]>(initial);

history.subscribe((entries) => saveHistory(entries));

export function addEntry(entry: Omit<HistoryEntry, 'id' | 'timestamp'>): void {
  history.update((entries) => {
    const newEntry: HistoryEntry = {
      ...entry,
      id: crypto.randomUUID(),
      timestamp: Date.now(),
    };
    return [newEntry, ...entries].slice(0, MAX_ENTRIES);
  });
}

export function clearHistory(): void {
  history.set([]);
}
