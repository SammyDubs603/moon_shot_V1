from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


ActionType = Literal["BUY", "HOLD", "EXIT"]


class Holding(BaseModel):
    asset: str
    amount: float
    price_usd: float | None = None
    usd_value: float


class PortfolioSnapshot(BaseModel):
    ts: datetime
    total_usd: float
    breakdown: list[Holding] = Field(default_factory=list)


class AssetBrief(BaseModel):
    symbol: str
    action: ActionType
    size_usd: float
    stop_price: float | None
    reasons: list[str] = Field(default_factory=list)
    indicators: dict[str, float | bool | str] = Field(default_factory=dict)


class TradeBriefPayload(BaseModel):
    regime: Literal["RISK_ON", "RISK_OFF"]
    generated_at: datetime
    assets: list[AssetBrief]


class TradeBriefRow(BaseModel):
    id: int | None = None
    ts: datetime
    venue: str = "coinbase"
    payload: TradeBriefPayload


class AISummary(BaseModel):
    id: int | None = None
    ts: datetime
    brief_id: int
    summary_text: str
    changes_text: str


class OverviewResponse(BaseModel):
    snapshot: PortfolioSnapshot | None = None
    brief: TradeBriefRow | None = None
    ai_summary: AISummary | None = None


class RunDailyResponse(BaseModel):
    status: str
    snapshot: PortfolioSnapshot
    brief: TradeBriefRow
    ai_summary: AISummary


class Candle(BaseModel):
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


class Quote(BaseModel):
    symbol: str
    price: float


class CoinbaseAccount(BaseModel):
    currency: str
    available_balance: float
    hold: float = 0.0


class RequestMeta(BaseModel):
    source: Literal["live", "demo"]
    details: dict[str, Any] = Field(default_factory=dict)
