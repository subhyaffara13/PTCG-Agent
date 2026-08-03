from typing import Optional

def _get_bedrock_output_config_effort_ceiling(
    model: str,
) -> Optional[BedrockOutputConfigEffort]:
    try:
        model_info = get_cached_model_info()(
            model=model,
            custom_llm_provider="bedrock",
        )
    except Exception:
        return None

    ceiling = model_info.get("bedrock_output_config_effort_ceiling")
    if isinstance(ceiling, str) and ceiling in _BEDROCK_OUTPUT_CONFIG_EFFORT_ORDER:
        return ceiling  # type: ignore[return-value]

    model_cost_key = model_info.get("key")
    if not isinstance(model_cost_key, str):
        return None

    local_model_info = _get_local_model_cost_map().get(model_cost_key, {})
    ceiling = local_model_info.get("bedrock_output_config_effort_ceiling")
    if isinstance(ceiling, str) and ceiling in _BEDROCK_OUTPUT_CONFIG_EFFORT_ORDER:
        return ceiling  # type: ignore[return-value]
    return None

