from typing import Optional

def get_provider_info(
    model: str, custom_llm_provider: Optional[str]
) -> Optional[ProviderSpecificModelInfo]:
    ## PROVIDER-SPECIFIC INFORMATION
    # if custom_llm_provider == "predibase":
    #     _model_info["supports_response_schema"] = True
    provider_config: Optional[BaseLLMModelInfo] = None
    if custom_llm_provider and custom_llm_provider in LlmProvidersSet:
        # Check if the provider string exists in LlmProviders enum
        provider_config = ProviderConfigManager.get_provider_model_info(
            model=model, provider=LlmProviders(custom_llm_provider)
        )

    model_info: Optional[ProviderSpecificModelInfo] = None
    if provider_config:
        model_info = provider_config.get_provider_info(model=model)

    return model_info

