
def _get_realtime_http_provider_config(
    custom_llm_provider: str,
    dynamic_api_base: Optional[str],
    dynamic_api_key: Optional[str],
    litellm_params: GenericLiteLLMParams,
) -> tuple[Any, str, str]:
    """
    Return (provider_config, resolved_api_base, resolved_api_key) for the
    realtime HTTP endpoints (client_secrets / realtime_calls).

    Uses ProviderConfigManager so each provider keeps its credential-resolution
    and URL-construction logic in its own transformation class.
    """
    from litellm.llms.base_llm.realtime.http_transformation import (
        BaseRealtimeHTTPConfig,
    )

    provider_config: Optional[BaseRealtimeHTTPConfig] = None
    if custom_llm_provider in LlmProviders._member_map_.values():
        provider_config = ProviderConfigManager.get_provider_realtime_http_config(
            model="",
            provider=LlmProviders(custom_llm_provider),
        )

    raw_api_base = dynamic_api_base or litellm_params.api_base
    raw_api_key = dynamic_api_key or litellm_params.api_key

    if provider_config is not None:
        resolved_api_base = provider_config.get_api_base(api_base=raw_api_base)
        resolved_api_key = provider_config.get_api_key(api_key=raw_api_key)
    else:
        # Fallback for providers without a dedicated HTTP config (treated as OpenAI-compatible).
        resolved_api_base = raw_api_base or litellm.api_base or "https://api.openai.com"
        resolved_api_key = (
            raw_api_key
            or litellm.api_key
            or litellm.openai_key
            or get_secret_str("OPENAI_API_KEY")
            or ""
        )

    return provider_config, resolved_api_base.rstrip("/"), resolved_api_key

