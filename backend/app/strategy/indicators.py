from __future__ import annotations

import math


def sma(values: list[float], window: int) -> float:
    if len(values) < window:
        return sum(values) / max(1, len(values))
    return sum(values[-window:]) / window


def roc(values: list[float], period: int = 12) -> float:
    if len(values) <= period:
        return 0.0
    base = values[-period - 1]
    if base == 0:
        return 0.0
    return (values[-1] - base) / base


def rsi(values: list[float], period: int = 14) -> float:
    if len(values) < period + 1:
        return 50.0
    gains = []
    losses = []
    for i in range(-period, 0):
        diff = values[i] - values[i - 1]
        gains.append(max(diff, 0))
        losses.append(abs(min(diff, 0)))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def atr(highs: list[float], lows: list[float], closes: list[float], period: int = 14) -> float:
    if len(closes) < 2:
        return 0.0
    trs = []
    for i in range(1, len(closes)):
        tr = max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1]))
        trs.append(tr)
    if not trs:
        return 0.0
    if len(trs) < period:
        return sum(trs) / len(trs)
    return sum(trs[-period:]) / period


def realized_vol(values: list[float], period: int = 20) -> float:
    if len(values) < period + 1:
        return 0.0
    rets = []
    for i in range(-period, 0):
        prev = values[i - 1]
        if prev == 0:
            continue
        rets.append(math.log(values[i] / prev))
    if not rets:
        return 0.0
    mean = sum(rets) / len(rets)
    var = sum((r - mean) ** 2 for r in rets) / len(rets)
    return math.sqrt(var) * math.sqrt(252)
