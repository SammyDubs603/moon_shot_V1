'use client';

import { useEffect, useState } from 'react';
import { getBriefs } from '@/lib/api';
import { LoginGate } from '@/components/LoginGate';

export default function BriefPage() {
  const [brief, setBrief] = useState<any>(null);
  const [authed, setAuthed] = useState(false);
  async function load() {
    try {
      const data = await getBriefs(1);
      setBrief(data.items?.[0]);
      setAuthed(true);
    } catch { setAuthed(false); }
  }
  useEffect(() => { load(); }, []);
  if (!authed) return <LoginGate onAuthed={load} />;

  return <div className="space-y-4">{brief?.payload?.assets?.map((asset: any) => <div className="card" key={asset.symbol}><h3>{asset.symbol} — {asset.action}</h3><ul className="list-disc pl-5 text-sm text-muted">{asset.reasons.map((r: string, i: number) => <li key={i}>{r}</li>)}</ul></div>)}</div>;
}
