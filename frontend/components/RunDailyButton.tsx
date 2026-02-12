'use client';

import { useState } from 'react';
import { runDaily } from '@/lib/api';

export function RunDailyButton() {
  const [status, setStatus] = useState<string>('');
  return (
    <div className="flex items-center gap-2">
      <button
        className="rounded-xl bg-blue-600 px-4 py-2 text-sm font-medium hover:bg-blue-500"
        onClick={async () => {
          setStatus('Running...');
          try {
            await runDaily();
            setStatus('Done');
          } catch {
            setStatus('Failed');
          }
        }}
      >
        Run Daily
      </button>
      <span className="text-sm text-muted">{status}</span>
    </div>
  );
}
