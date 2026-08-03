import copy
from typing import List, Optional

def get_valid_models(
    check_provider_endpoint: Optional[bool] = None,
    custom_llm_provider: Optional[str] = None,
    litellm_params: Optional[LiteLLM_Params] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
) -> List[str]:
    """
    Returns a list of valid LLMs based on the set environment variables

    Args:
        check_provider_endpoint: If True, will check the provider's endpoint for valid models.
        custom_llm_provider: If provided, will only check the provider's endpoint for valid models.
        api_key: If provided, will use the API key to get valid models.
        api_base: If provided, will use the API base to get valid models.
    Returns:
        A list of valid LLMs
    """

    try:
        ################################
        # init litellm_params
        #################################
        from litellm.types.router import LiteLLM_Params

        if litellm_params is None:
            litellm_params = LiteLLM_Params(model="")
        if api_key is not None:
            litellm_params.api_key = api_key
        if api_base is not None:
            litellm_params.api_base = api_base
        #################################

        check_provider_endpoint = (
            check_provider_endpoint or litellm.check_provider_endpoint
        )
        # get keys set in .env

        valid_providers: List[str] = []
        valid_models: List[str] = []
        # for all valid providers, make a list of supported llms

        if custom_llm_provider:
            valid_providers = [custom_llm_provider]
        else:
            valid_providers = _infer_valid_provider_from_env_vars(custom_llm_provider)

        for provider in valid_providers:
            provider_config = ProviderConfigManager.get_provider_model_info(
                model=None,
                provider=LlmProviders(provider),
            )

            if custom_llm_provider and provider != custom_llm_provider:
                continue

            if provider == "azure":
                valid_models.append("Azure-LLM")
            elif (
                provider_config is not None
                and check_provider_endpoint
                and provider is not None
            ):
                valid_models.extend(
                    _get_valid_models_from_provider_api(
                        provider_config,
                        provider,
                        litellm_params,
                    )
                )
            else:
                models_for_provider = copy.deepcopy(
                    litellm.models_by_provider.get(provider, [])
                )
                valid_models.extend(models_for_provider)

        return valid_models
    except Exception as e:
        verbose_logger.warning(f"Error getting valid models: {e}")
        return []  # NON-Blocking

