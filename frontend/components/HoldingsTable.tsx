import { Holding } from '@/lib/api';

export function HoldingsTable({ items }: { items: Holding[] }) {
  return (
    <div className="card">
      <h3 className="mb-3 text-lg font-semibold">Holdings</h3>
      <table className="w-full text-sm">
        <thead className="text-muted">
          <tr><th className="text-left">Asset</th><th className="text-right">Amount</th><th className="text-right">Price</th><th className="text-right">USD Value</th></tr>
        </thead>
        <tbody>
          {items.map((h) => (
            <tr key={h.asset} className="border-t border-border">
              <td className="py-2">{h.asset}</td>
              <td className="text-right">{h.amount.toFixed(6)}</td>
              <td className="text-right">${(h.price_usd || 0).toFixed(2)}</td>
              <td className="text-right">${h.usd_value.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
