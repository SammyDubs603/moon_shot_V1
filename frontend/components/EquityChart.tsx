'use client';

import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

export function EquityChart({ data }: { data: { ts: string; total_usd: number }[] }) {
  return (
    <div className="card h-72">
      <h3 className="mb-2 text-lg font-semibold">Equity Curve</h3>
      <ResponsiveContainer width="100%" height="90%">
        <LineChart data={data.slice().reverse()}>
          <XAxis dataKey="ts" tickFormatter={(v) => new Date(v).toLocaleDateString()} />
          <YAxis domain={['auto', 'auto']} />
          <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} labelFormatter={(v) => new Date(v).toLocaleString()} />
          <Line type="monotone" dataKey="total_usd" stroke="#60a5fa" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
