from app.strategy.risk import is_risk_off


def test_risk_off_when_vol_high():
    risk_off, reasons = is_risk_off(1.5, 0.03)
    assert risk_off
    assert reasons


def test_risk_on_when_metrics_ok():
    risk_off, reasons = is_risk_off(0.4, 0.02)
    assert not risk_off
    assert reasons == []
