from typing import Optional

def _should_allow_input_examples(
    custom_llm_provider: Optional[str], model: str
) -> bool:
    if custom_llm_provider == "anthropic":
        return True
    if (
        custom_llm_provider == "azure_ai"
        or custom_llm_provider == "bedrock"
        or custom_llm_provider == "vertex_ai"
    ):
        return "claude" in model.lower()
    return False

