from typing import Optional, Tuple

def _get_provider_token_counter(
    deployment: dict, model_to_use: str
) -> Tuple[Optional[BaseTokenCounter], Optional[str], Optional[str]]:
    """
    Auto-route to the correct provider's token counter based on model/deployment.
    Uses the existing get_provider_model_info infrastructure with switch-case pattern.
    """
    if deployment is None:
        return None

    from litellm.litellm_core_utils.get_llm_provider_logic import get_llm_provider

    full_model = deployment.get("litellm_params", {}).get("model", "")
    model: Optional[str] = None
    custom_llm_provider: Optional[str] = None

    try:
        # Use existing LiteLLM logic to determine provider
        model, custom_llm_provider, dynamic_api_key, api_base = get_llm_provider(
            model=full_model,
            custom_llm_provider=deployment.get("litellm_params", {}).get(
                "custom_llm_provider"
            ),
            api_base=deployment.get("litellm_params", {}).get("api_base"),
            api_key=deployment.get("litellm_params", {}).get("api_key"),
        )

        # Switch case pattern using existing get_provider_model_info
        from litellm.types.utils import LlmProviders
        from litellm.utils import ProviderConfigManager

        # Convert string provider to LlmProviders enum
        llm_provider_enum = LlmProviders(custom_llm_provider)
        # Add more provider mappings as needed

        if llm_provider_enum:
            provider_model_info = ProviderConfigManager.get_provider_model_info(
                model=full_model, provider=llm_provider_enum
            )
            if provider_model_info is not None:
                return (
                    provider_model_info.get_token_counter(),
                    model,
                    custom_llm_provider,
                )

    except Exception:
        # If provider detection fails, fall back to manual checks
        if full_model.startswith("anthropic/") or "anthropic" in full_model.lower():
            from litellm.llms.anthropic.common_utils import AnthropicModelInfo

            anthropic_model_info = AnthropicModelInfo()
            return anthropic_model_info.get_token_counter(), model, custom_llm_provider

    return None, None, None

