
def _resolve_model_provider_for_responses(
    model: str,
    custom_llm_provider: Optional[str],
    litellm_params: GenericLiteLLMParams,
    local_vars: Dict[str, Any],
) -> tuple[str, Optional[str]]:
    if custom_llm_provider is not None and not litellm_params.custom_llm_provider:
        litellm_params.custom_llm_provider = custom_llm_provider
    (
        model,
        custom_llm_provider,
        dynamic_api_key,
        dynamic_api_base,
    ) = litellm.get_llm_provider(
        model=model,
        litellm_params=litellm_params,
    )
    local_vars["custom_llm_provider"] = custom_llm_provider
    if dynamic_api_key is not None:
        litellm_params.api_key = dynamic_api_key
    if dynamic_api_base is not None:
        litellm_params.api_base = dynamic_api_base
    return model, custom_llm_provider

