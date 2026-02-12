export type Holding = { asset: string; amount: number; price_usd?: number; usd_value: number };
export type Snapshot = { ts: string; total_usd: number; breakdown: Holding[] };
export type AssetBrief = { symbol: string; action: 'BUY' | 'HOLD' | 'EXIT'; size_usd: number; stop_price?: number | null; reasons: string[] };
export type Brief = { id?: number; ts: string; venue: string; payload: { regime: string; generated_at: string; assets: AssetBrief[] } };
export type AISummary = { summary_text: string; changes_text: string; ts: string };

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export async function getOverview() {
  const res = await fetch(`${BASE_URL}/api/overview`, { cache: 'no-store', credentials: 'include' });
  if (!res.ok) throw new Error('Failed to load overview');
  return res.json();
}

export async function getSnapshots(limit = 120) {
  const res = await fetch(`${BASE_URL}/api/snapshots?limit=${limit}`, { cache: 'no-store', credentials: 'include' });
  if (!res.ok) throw new Error('Failed snapshots');
  return res.json();
}

export async function getBriefs(limit = 30) {
  const res = await fetch(`${BASE_URL}/api/briefs?limit=${limit}`, { cache: 'no-store', credentials: 'include' });
  if (!res.ok) throw new Error('Failed briefs');
  return res.json();
}

export async function runDaily() {
  const res = await fetch(`${BASE_URL}/api/run-daily`, { method: 'POST', credentials: 'include' });
  if (!res.ok) throw new Error('run daily failed');
  return res.json();
}
