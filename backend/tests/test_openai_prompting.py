from app.openai_client import SYSTEM_PROMPT


def test_system_prompt_has_guardrails():
    lower = SYSTEM_PROMPT.lower()
    assert "do not provide financial advice" in lower
    assert "do not invent numbers" in lower
    assert "only use provided data" in lower
