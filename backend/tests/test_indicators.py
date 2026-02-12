from app.strategy.indicators import sma, rsi, roc, atr


def test_sma():
    assert sma([1, 2, 3, 4, 5], 3) == 4


def test_rsi_bounds():
    value = rsi([float(i) for i in range(1, 30)], 14)
    assert 0 <= value <= 100


def test_roc_positive():
    assert roc([1, 1.1, 1.3, 1.5, 1.8, 2.0], 3) > 0


def test_atr_nonnegative():
    highs = [10, 11, 12, 13]
    lows = [9, 10, 11, 12]
    closes = [9.5, 10.5, 11.5, 12.5]
    assert atr(highs, lows, closes) >= 0
