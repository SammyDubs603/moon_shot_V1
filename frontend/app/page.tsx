'use client';

import { useEffect, useState } from 'react';
import { AISummaryPanel } from '@/components/AISummaryPanel';
import { BriefCards } from '@/components/BriefCards';
import { EquityChart } from '@/components/EquityChart';
import { HoldingsTable } from '@/components/HoldingsTable';
import { LoginGate } from '@/components/LoginGate';
import { RunDailyButton } from '@/components/RunDailyButton';
import { getOverview, getSnapshots } from '@/lib/api';

export default function HomePage() {
  const [overview, setOverview] = useState<any>(null);
  const [snapshots, setSnapshots] = useState<any[]>([]);
  const [authed, setAuthed] = useState(false);

  async function load() {
    try {
      const [o, s] = await Promise.all([getOverview(), getSnapshots(120)]);
      setOverview(o);
      setSnapshots(s.items || []);
      setAuthed(true);
    } catch {
      setAuthed(false);
    }
  }

  useEffect(() => { load(); }, []);

  if (!authed) return <LoginGate onAuthed={load} />;

  return (
    <div className="space-y-4">
      <div className="card flex items-center justify-between">
        <div>
          <p className="text-sm text-muted">Total Portfolio (USD)</p>
          <p className="text-3xl font-bold">${overview?.snapshot?.total_usd?.toFixed(2) || '0.00'}</p>
        </div>
        <RunDailyButton />
      </div>
      <EquityChart data={snapshots} />
      <HoldingsTable items={overview?.snapshot?.breakdown || []} />
      <BriefCards assets={overview?.brief?.payload?.assets || []} />
      <AISummaryPanel summary={overview?.ai_summary} />
    </div>
  );
}
