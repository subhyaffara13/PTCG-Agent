from typing import Optional

def _cached_get_model_info_helper(
    model: str,
    custom_llm_provider: Optional[str],
    api_base: Optional[str] = None,
) -> ModelInfoBase:
    """
    _get_model_info_helper wrapped with lru_cache

    Speed Optimization to hit high RPS
    """
    return _get_model_info_helper(
        model=model,
        custom_llm_provider=custom_llm_provider,
        api_base=api_base,
    )

