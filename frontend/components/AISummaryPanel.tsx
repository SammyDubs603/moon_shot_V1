import { AISummary } from '@/lib/api';

export function AISummaryPanel({ summary }: { summary?: AISummary }) {
  return (
    <div className="card">
      <h3 className="mb-2 text-lg font-semibold">AI Summary</h3>
      <p className="text-sm text-muted">{summary?.summary_text || 'No summary yet.'}</p>
      <p className="mt-3 text-sm text-muted">{summary?.changes_text || 'Run daily job to get changes.'}</p>
    </div>
  );
}
