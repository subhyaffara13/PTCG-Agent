
def get_supported_regions(
    model: str, custom_llm_provider: Optional[str] = None
) -> Optional[List[str]]:
    """
    Get a list of supported regions for a given model and provider.

    Parameters:
    model (str): The model name to be checked.
    custom_llm_provider (Optional[str]): The provider to be checked.
    """
    try:
        model, custom_llm_provider, _, _ = litellm.get_llm_provider(
            model=model, custom_llm_provider=custom_llm_provider
        )

        model_info = _get_model_info_helper(
            model=model, custom_llm_provider=custom_llm_provider
        )

        # Get the key used in model_cost to look up supported_regions
        # since ModelInfoBase doesn't include this field
        model_key = model_info.get("key")
        if model_key is None:
            return None

        model_cost_data = litellm.model_cost.get(model_key, {})
        supported_regions = model_cost_data.get("supported_regions", None)
        if supported_regions is None:
            return None

        #########################################################
        # Ensure only list supported regions are returned
        #########################################################
        if isinstance(supported_regions, list):
            return supported_regions
        else:
            return None
    except Exception as e:
        verbose_logger.debug(
            f"Model not found or error in checking supported_regions support. You passed model={model}, custom_llm_provider={custom_llm_provider}. Error: {str(e)}"
        )
        return None

