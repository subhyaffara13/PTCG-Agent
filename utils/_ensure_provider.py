from typing import Optional

def _ensure_provider(custom_llm_provider: Optional[str]) -> str:
    return custom_llm_provider or "openai"

