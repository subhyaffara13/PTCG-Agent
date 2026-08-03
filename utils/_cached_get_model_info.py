from typing import Optional

def _cached_get_model_info(
    model: str,
    custom_llm_provider: Optional[str] = None,
    api_base: Optional[str] = None,
) -> ModelInfo:
    return _build_model_info(
        model=model, custom_llm_provider=custom_llm_provider, api_base=api_base
    )

