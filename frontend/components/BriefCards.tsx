import { AssetBrief } from '@/lib/api';

const colorMap: Record<string, string> = { BUY: 'text-green-400', HOLD: 'text-yellow-300', EXIT: 'text-red-400' };

export function BriefCards({ assets }: { assets: AssetBrief[] }) {
  return (
    <div className="grid gap-3 md:grid-cols-2">
      {assets.map((asset) => (
        <div key={asset.symbol} className="card">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">{asset.symbol}</h3>
            <span className={`font-bold ${colorMap[asset.action]}`}>{asset.action}</span>
          </div>
          <p className="text-sm text-muted">Size: ${asset.size_usd.toFixed(2)} {asset.stop_price ? `• Stop: $${asset.stop_price}` : ''}</p>
          <ul className="mt-2 list-disc pl-5 text-sm text-muted">
            {asset.reasons.map((r, idx) => <li key={idx}>{r}</li>)}
          </ul>
        </div>
      ))}
    </div>
  );
}
