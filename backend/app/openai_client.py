from __future__ import annotations

import json
from typing import Any

from openai import OpenAI

from app.config import get_settings

SYSTEM_PROMPT = (
    "You are an analyst summarizing a trading system’s outputs. "
    "Do not provide financial advice. Do not invent numbers. Only use provided data."
)


def summarize_brief(today_brief: dict[str, Any], yesterday_brief_optional: dict[str, Any] | None, portfolio_snapshot_optional: dict[str, Any] | None) -> dict[str, str]:
    settings = get_settings()
    if not settings.openai_api_key:
        return {
            "summary_text": "OpenAI key not configured. Summary unavailable in this environment.",
            "changes_text": "No model comparison generated.",
        }

    client = OpenAI(api_key=settings.openai_api_key)
    payload = {
        "today_brief": today_brief,
        "yesterday_brief": yesterday_brief_optional,
        "portfolio_snapshot": portfolio_snapshot_optional,
    }

    prompt = (
        "Summarize today's deterministic trade brief for a private dashboard. "
        "First paragraph: explain actions/reasons/risk in plain English. "
        "Second paragraph: what changed since yesterday. "
        "If yesterday is missing, say so. Keep concise. Data:\n"
        + json.dumps(payload, default=str)
    )

    response = client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    text = response.output_text.strip()
    blocks = [b.strip() for b in text.split("\n\n") if b.strip()]
    summary = blocks[0] if blocks else text
    changes = blocks[1] if len(blocks) > 1 else "No explicit change block returned."
    return {"summary_text": summary, "changes_text": changes}
