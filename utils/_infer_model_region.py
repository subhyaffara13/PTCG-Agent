
def _infer_model_region(litellm_params: LiteLLM_Params) -> Optional[AllowedModelRegion]:
    """
    Infer if a model is in the EU or US region

    Returns:
    - str (region) - "eu" or "us"
    - None (if region not found)
    """
    model, custom_llm_provider, _, _ = litellm.get_llm_provider(
        model=litellm_params.model, litellm_params=litellm_params
    )

    model_region = _get_model_region(
        custom_llm_provider=custom_llm_provider, litellm_params=litellm_params
    )

    if model_region is None:
        verbose_logger.debug(
            "Cannot infer model region for model: {}".format(litellm_params.model)
        )
        return None

    if custom_llm_provider == "azure":
        eu_regions = litellm.AzureOpenAIConfig().get_eu_regions()
        us_regions = litellm.AzureOpenAIConfig().get_us_regions()
    elif custom_llm_provider == "vertex_ai":
        eu_regions = litellm.VertexAIConfig().get_eu_regions()
        us_regions = litellm.VertexAIConfig().get_us_regions()
    elif custom_llm_provider == "bedrock":
        eu_regions = litellm.AmazonBedrockGlobalConfig().get_eu_regions()
        us_regions = litellm.AmazonBedrockGlobalConfig().get_us_regions()
    elif custom_llm_provider == "watsonx":
        eu_regions = litellm.IBMWatsonXAIConfig().get_eu_regions()
        us_regions = litellm.IBMWatsonXAIConfig().get_us_regions()
    else:
        eu_regions = []
        us_regions = []

    for region in eu_regions:
        if region in model_region.lower():
            return "eu"
    for region in us_regions:
        if region in model_region.lower():
            return "us"
    return None

