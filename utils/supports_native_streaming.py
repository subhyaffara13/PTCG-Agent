
def supports_native_streaming(model: str, custom_llm_provider: Optional[str]) -> bool:
    """
    Check if the given model supports native streaming and return a boolean value.

    Parameters:
    model (str): The model name to be checked.
    custom_llm_provider (str): The provider to be checked.

    Returns:
    bool: True if the model supports native streaming, False otherwise.

    Raises:
    Exception: If the given model is not found in model_prices_and_context_window.json.
    """
    try:
        model, custom_llm_provider, _, _ = litellm.get_llm_provider(
            model=model, custom_llm_provider=custom_llm_provider
        )

        model_info = _get_model_info_helper(
            model=model, custom_llm_provider=custom_llm_provider
        )
        supports_native_streaming = model_info.get("supports_native_streaming", True)
        if supports_native_streaming is None:
            supports_native_streaming = True
        return supports_native_streaming
    except Exception as e:
        verbose_logger.debug(
            f"Model not found or error in checking supports_native_streaming support. You passed model={model}, custom_llm_provider={custom_llm_provider}. Error: {str(e)}"
        )
        return False

