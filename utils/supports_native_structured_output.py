from typing import Optional

def supports_native_structured_output(
    model: str, custom_llm_provider: Optional[str] = None
) -> bool:
    """
    Check if the given model supports native structured outputs and return a boolean value.
    """
    return _supports_factory(
        model=model,
        custom_llm_provider=custom_llm_provider,
        key="supports_native_structured_output",
    )

