from typing import Optional

def _check_provider_match(model_info: dict, custom_llm_provider: Optional[str]) -> bool:
    """
    Check if the model info provider matches the custom provider.

    A missing ``litellm_provider`` key and a ``litellm_provider`` set to
    ``None`` both mean "no specific provider constraint" and are treated
    as a wildcard match. ``register_model`` may persist ``None`` here via
    ``get_model_info`` when a deployment is registered without a provider,
    so normalising the two cases keeps custom pricing applied consistently.
    """
    if custom_llm_provider and (
        model_info.get("litellm_provider") is not None
        and model_info["litellm_provider"] != custom_llm_provider
    ):
        if custom_llm_provider == "vertex_ai" and model_info[
            "litellm_provider"
        ].startswith("vertex_ai"):
            return True
        elif custom_llm_provider == "fireworks_ai" and model_info[
            "litellm_provider"
        ].startswith("fireworks_ai"):
            return True
        elif custom_llm_provider.startswith("bedrock") and model_info[
            "litellm_provider"
        ].startswith("bedrock"):
            return True
        elif (
            custom_llm_provider == "litellm_proxy"
        ):  # litellm_proxy is a special case, it's not a provider, it's a proxy for the provider
            return True
        elif custom_llm_provider == "azure_ai" and model_info["litellm_provider"] in (
            "azure",
            "openai",
        ):
            # Azure AI also works with azure models
            # as a last attempt if the model is not on Azure AI, Azure then fallback to OpenAI cost
            # tracking the cost is better than attributing 0 cost to it.
            return True
        elif custom_llm_provider == "github":
            # Allow github/<model> aliases to reuse existing provider metadata.
            return True
        else:
            return False

    return True

