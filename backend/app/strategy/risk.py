from __future__ import annotations


def is_risk_off(realized_vol: float, atr_pct: float) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if realized_vol > 1.2:
        reasons.append(f"Realized volatility too high ({realized_vol:.2f})")
    if atr_pct > 0.08:
        reasons.append(f"ATR percentage too high ({atr_pct:.2%})")
    return (len(reasons) > 0, reasons)
