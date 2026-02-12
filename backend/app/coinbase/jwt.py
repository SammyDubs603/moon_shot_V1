from __future__ import annotations

from datetime import datetime, timedelta, timezone

import jwt


def generate_coinbase_jwt(api_key: str, api_secret: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": api_key,
        "iss": "coinbase-cloud",
        "nbf": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=2)).timestamp()),
    }
    return jwt.encode(payload, api_secret, algorithm="HS256")
