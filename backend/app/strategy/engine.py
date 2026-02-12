from __future__ import annotations

from datetime import datetime, timezone

from app.models import AssetBrief, Candle, TradeBriefPayload
from app.strategy.indicators import atr, realized_vol, roc, rsi, sma
from app.strategy.risk import is_risk_off


def generate_asset_brief(symbol: str, candles: list[Candle], portfolio_value: float) -> AssetBrief:
    closes = [c.close for c in candles]
    highs = [c.high for c in candles]
    lows = [c.low for c in candles]
    price = closes[-1]
    ma50 = sma(closes, 50)
    ma200 = sma(closes, 200)
    rsi_val = rsi(closes)
    roc_val = roc(closes, 12)
    atr_val = atr(highs, lows, closes)
    atr_pct = atr_val / price if price else 0
    vol = realized_vol(closes)

    risk_off, risk_reasons = is_risk_off(vol, atr_pct)
    reasons = [
        f"MA50={ma50:.2f}, MA200={ma200:.2f}",
        f"RSI={rsi_val:.1f}, ROC12={roc_val:.2%}",
        f"ATR%={atr_pct:.2%}, RVOL={vol:.2f}",
    ]

    if risk_off:
        reasons.extend(risk_reasons)
        return AssetBrief(
            symbol=symbol,
            action="HOLD",
            size_usd=0,
            stop_price=None,
            reasons=reasons,
            indicators={"ma50": ma50, "ma200": ma200, "rsi": rsi_val, "roc": roc_val, "atr_pct": atr_pct, "realized_vol": vol},
        )

    trending_up = ma50 > ma200 and price > ma50
    momentum_up = rsi_val >= 52 and roc_val > 0
    if trending_up and momentum_up:
        size = max(100.0, portfolio_value * 0.05)
        return AssetBrief(
            symbol=symbol,
            action="BUY",
            size_usd=round(size, 2),
            stop_price=round(price * 0.93, 2),
            reasons=reasons + ["Trend and momentum aligned."],
            indicators={"ma50": ma50, "ma200": ma200, "rsi": rsi_val, "roc": roc_val, "atr_pct": atr_pct, "realized_vol": vol},
        )

    if ma50 < ma200 and rsi_val < 45:
        return AssetBrief(
            symbol=symbol,
            action="EXIT",
            size_usd=0,
            stop_price=None,
            reasons=reasons + ["Downtrend with weak momentum."],
            indicators={"ma50": ma50, "ma200": ma200, "rsi": rsi_val, "roc": roc_val, "atr_pct": atr_pct, "realized_vol": vol},
        )

    return AssetBrief(
        symbol=symbol,
        action="HOLD",
        size_usd=0,
        stop_price=round(price * 0.9, 2),
        reasons=reasons + ["Signals mixed; no edge."],
        indicators={"ma50": ma50, "ma200": ma200, "rsi": rsi_val, "roc": roc_val, "atr_pct": atr_pct, "realized_vol": vol},
    )


def generate_trade_brief(candle_map: dict[str, list[Candle]], portfolio_value: float) -> TradeBriefPayload:
    briefs = [generate_asset_brief(symbol, candles, portfolio_value) for symbol, candles in candle_map.items()]
    regime = "RISK_OFF" if all(item.action == "HOLD" and item.size_usd == 0 for item in briefs) else "RISK_ON"
    return TradeBriefPayload(regime=regime, generated_at=datetime.now(timezone.utc), assets=briefs)
