from typing import List, Optional

def get_provider_models(
    provider: str, litellm_params: Optional[LiteLLM_Params] = None
) -> Optional[List[str]]:
    """
    Returns the list of known models by provider
    """
    if provider == "*":
        return get_valid_models(litellm_params=litellm_params)

    if provider in litellm.models_by_provider:
        provider_models = get_valid_models(
            custom_llm_provider=provider, litellm_params=litellm_params
        )
        return provider_models
    return None

