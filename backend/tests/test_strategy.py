from datetime import datetime, timezone, timedelta

from app.models import Candle
from app.strategy.engine import generate_asset_brief


def mk_candles(base: float, slope: float, days: int = 260):
    now = datetime.now(timezone.utc)
    candles = []
    for i in range(days):
        close = base + i * slope
        candles.append(
            Candle(
                ts=now - timedelta(days=days - i),
                open=close * 0.99,
                high=close * 1.02,
                low=close * 0.98,
                close=close,
                volume=100,
            )
        )
    return candles


def test_buy_signal_in_uptrend():
    brief = generate_asset_brief("BTC-USD", mk_candles(100, 2), 10000)
    assert brief.action in {"BUY", "HOLD"}


def test_exit_signal_in_downtrend():
    brief = generate_asset_brief("ETH-USD", mk_candles(3000, -5), 10000)
    assert brief.action in {"EXIT", "HOLD"}
