from __future__ import annotations

from datetime import datetime, timezone

from app.coinbase.client import CoinbaseClient
from app import db
from app.models import AISummary, Holding, PortfolioSnapshot, TradeBriefRow
from app.openai_client import summarize_brief
from app.strategy.engine import generate_trade_brief


def build_snapshot(client: CoinbaseClient) -> PortfolioSnapshot:
    accounts = client.list_accounts()
    holdings: list[Holding] = []
    total = 0.0
    for account in accounts:
        symbol = f"{account.currency}-USD"
        price = 1.0 if account.currency in {"USD", "USDC"} else client.get_spot_quote(symbol).price
        usd_value = account.available_balance * price
        total += usd_value
        holdings.append(Holding(asset=account.currency, amount=account.available_balance, price_usd=price, usd_value=round(usd_value, 2)))
    return PortfolioSnapshot(ts=datetime.now(timezone.utc), total_usd=round(total, 2), breakdown=holdings)


def run_daily_job() -> tuple[PortfolioSnapshot, TradeBriefRow, AISummary]:
    db.migrate()
    client = CoinbaseClient()

    snapshot = build_snapshot(client)
    db.insert_snapshot(snapshot)

    candles = {"BTC-USD": client.get_candles("BTC-USD"), "ETH-USD": client.get_candles("ETH-USD")}
    brief_payload = generate_trade_brief(candles, snapshot.total_usd)
    brief_row = TradeBriefRow(ts=datetime.now(timezone.utc), venue="coinbase", payload=brief_payload)
    brief_id = db.insert_brief(brief_row)
    brief_row.id = brief_id

    prev = db.previous_brief(exclude_id=brief_id)
    summary_payload = summarize_brief(
        today_brief=brief_row.model_dump(),
        yesterday_brief_optional=prev.model_dump() if prev else None,
        portfolio_snapshot_optional=snapshot.model_dump(),
    )
    ai_summary = AISummary(
        ts=datetime.now(timezone.utc),
        brief_id=brief_id,
        summary_text=summary_payload["summary_text"],
        changes_text=summary_payload["changes_text"],
    )
    ai_id = db.insert_ai_summary(ai_summary)
    ai_summary.id = ai_id
    return snapshot, brief_row, ai_summary
