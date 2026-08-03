from typing import Optional

def supports_reasoning(model: str, custom_llm_provider: Optional[str] = None) -> bool:
    """
    Check if the given model supports reasoning and return a boolean value.
    """
    return _supports_factory(
        model=model, custom_llm_provider=custom_llm_provider, key="supports_reasoning"
    )

