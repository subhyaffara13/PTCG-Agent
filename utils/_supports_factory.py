
def _supports_factory(model: str, custom_llm_provider: Optional[str], key: str) -> bool:
    """
    Check if the given model supports function calling and return a boolean value.

    Parameters:
    model (str): The model name to be checked.
    custom_llm_provider (Optional[str]): The provider to be checked.

    Returns:
    bool: True if the model supports function calling, False otherwise.

    Raises:
    Exception: If the given model is not found or there's an error in retrieval.
    """
    try:
        model, custom_llm_provider, _, _ = litellm.get_llm_provider(
            model=model, custom_llm_provider=custom_llm_provider
        )

        model_info = _get_model_info_helper(
            model=model, custom_llm_provider=custom_llm_provider
        )

        if model_info.get(key, False) is True:
            return True
        elif model_info.get(key) is None:  # don't check if 'False' explicitly set
            # Fallback: when the provider-prefixed entry (e.g.
            # "deepseek/deepseek-chat") exists but is missing a capability
            # field, check the bare model-name entry (e.g. "deepseek-chat")
            # which may carry the complete metadata.  See #20885.
            bare_model_key = _get_model_cost_key(model)
            if bare_model_key is not None:
                bare_entry = litellm.model_cost.get(bare_model_key) or {}
                if bare_entry.get(key, False) is True:
                    return True

            supported_by_provider = _supports_provider_info_factory(
                model, custom_llm_provider, key
            )
            if supported_by_provider is not None:
                return supported_by_provider

        return False
    except Exception as e:
        verbose_logger.debug(
            f"Model not found or error in checking {key} support. You passed model={model}, custom_llm_provider={custom_llm_provider}. Error: {str(e)}"
        )

        supported_by_provider = _supports_provider_info_factory(
            model, custom_llm_provider, key
        )
        if supported_by_provider is not None:
            return supported_by_provider

        return False

