from typing import Optional

def _build_custom_pricing_entry(
    custom_llm_provider: str,
    kwargs: dict,
    model_info: Optional[dict] = None,
) -> dict:
    """Build a complete model cost entry from kwargs and model_info.

    Collects all CustomPricingLiteLLMParams fields present in kwargs and
    merges metadata from model_info (mode, supports_prompt_caching, max_tokens)
    so that register_model() receives the full pricing configuration.
    """
    entry: dict = {"litellm_provider": custom_llm_provider}

    for field_name in CustomPricingLiteLLMParams.model_fields:
        value = kwargs.get(field_name)
        if value is not None:
            entry[field_name] = value

    if model_info and isinstance(model_info, dict):
        for key in ("mode", "supports_prompt_caching", "max_tokens"):
            if key in model_info and model_info[key] is not None:
                entry.setdefault(key, model_info[key])

    return entry

