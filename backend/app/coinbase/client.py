from __future__ import annotations

import random
import time
from datetime import datetime, timedelta, timezone

import httpx

from app.coinbase.jwt import generate_coinbase_jwt
from app.config import get_settings
from app.models import Candle, CoinbaseAccount, Quote


class CoinbaseClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.demo_mode = not (self.settings.coinbase_api_key and self.settings.coinbase_api_secret)

    def _request(self, method: str, path: str, params: dict | None = None) -> dict:
        if self.demo_mode:
            raise RuntimeError("Live request attempted during demo mode")

        jwt_token = generate_coinbase_jwt(self.settings.coinbase_api_key or "", self.settings.coinbase_api_secret or "")
        headers = {"Authorization": f"Bearer {jwt_token}"}

        delay = 0.4
        for attempt in range(4):
            try:
                with httpx.Client(timeout=10) as client:
                    response = client.request(method, f"{self.settings.coinbase_api_host}{path}", headers=headers, params=params)
                    response.raise_for_status()
                    return response.json()
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(delay)
                delay *= 2
        raise RuntimeError("Unreachable")

    def list_accounts(self) -> list[CoinbaseAccount]:
        if self.demo_mode:
            return [
                CoinbaseAccount(currency="BTC", available_balance=0.42),
                CoinbaseAccount(currency="ETH", available_balance=3.1),
                CoinbaseAccount(currency="USDC", available_balance=1200),
            ]

        payload = self._request("GET", "/api/v3/brokerage/accounts")
        accounts: list[CoinbaseAccount] = []
        for item in payload.get("accounts", []):
            bal = float(item.get("available_balance", {}).get("value", 0.0))
            hold = float(item.get("hold", {}).get("value", 0.0))
            currency = item.get("currency", "")
            if bal > 0 or hold > 0:
                accounts.append(CoinbaseAccount(currency=currency, available_balance=bal, hold=hold))
        return accounts

    def get_spot_quote(self, symbol: str) -> Quote:
        if self.demo_mode:
            prices = {"BTC-USD": 68000.0 + random.uniform(-800, 900), "ETH-USD": 3500.0 + random.uniform(-60, 60), "USDC-USD": 1.0}
            return Quote(symbol=symbol, price=prices.get(symbol, 1.0))

        payload = self._request("GET", f"/api/v3/brokerage/products/{symbol}")
        return Quote(symbol=symbol, price=float(payload.get("price", 0.0)))

    def get_candles(self, symbol: str, days: int = 260) -> list[Candle]:
        if self.demo_mode:
            candles: list[Candle] = []
            base = 62000 if symbol == "BTC-USD" else 3000
            now = datetime.now(timezone.utc)
            for i in range(days):
                drift = i * (22 if symbol == "BTC-USD" else 1.5)
                noise = random.uniform(-1000, 1000) if symbol == "BTC-USD" else random.uniform(-120, 120)
                close = max(100.0, base + drift + noise)
                high = close * (1 + random.uniform(0.001, 0.02))
                low = close * (1 - random.uniform(0.001, 0.02))
                open_p = (high + low) / 2
                candles.append(Candle(ts=now - timedelta(days=days - i), open=open_p, high=high, low=low, close=close, volume=random.uniform(10, 200)))
            return candles

        end = int(datetime.now(timezone.utc).timestamp())
        start = int((datetime.now(timezone.utc) - timedelta(days=days + 5)).timestamp())
        payload = self._request(
            "GET",
            f"/api/v3/brokerage/products/{symbol}/candles",
            params={"granularity": "ONE_DAY", "start": str(start), "end": str(end)},
        )
        candles = [
            Candle(
                ts=datetime.fromtimestamp(int(c["start"]), timezone.utc),
                low=float(c["low"]),
                high=float(c["high"]),
                open=float(c["open"]),
                close=float(c["close"]),
                volume=float(c.get("volume", 0.0)),
            )
            for c in payload.get("candles", [])
        ]
        return sorted(candles, key=lambda c: c.ts)
