'use client';

import { useEffect, useState } from 'react';
import { EquityChart } from '@/components/EquityChart';
import { getSnapshots } from '@/lib/api';
import { LoginGate } from '@/components/LoginGate';

export default function HistoryPage() {
  const [items, setItems] = useState<any[]>([]);
  const [authed, setAuthed] = useState(false);
  async function load() {
    try {
      const data = await getSnapshots(180);
      setItems(data.items || []);
      setAuthed(true);
    } catch { setAuthed(false); }
  }
  useEffect(() => { load(); }, []);
  if (!authed) return <LoginGate onAuthed={load} />;

  return (
    <div className="space-y-4">
      <EquityChart data={items} />
      <div className="card overflow-auto">
        <table className="w-full text-sm"><tbody>{items.map((s) => <tr key={s.ts}><td>{new Date(s.ts).toLocaleString()}</td><td className="text-right">${s.total_usd.toFixed(2)}</td></tr>)}</tbody></table>
      </div>
    </div>
  );
}
