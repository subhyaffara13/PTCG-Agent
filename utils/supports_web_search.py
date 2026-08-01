
def supports_web_search(model: str, custom_llm_provider: Optional[str] = None) -> bool:
    """
    Check if the given model supports web search and return a boolean value.

    Parameters:
    model (str): The model name to be checked.
    custom_llm_provider (str): The provider to be checked.

    Returns:
    bool: True if the model supports web search, False otherwise.

    Raises:
    Exception: If the given model is not found in model_prices_and_context_window.json.
    """
    return _supports_factory(
        model=model,
        custom_llm_provider=custom_llm_provider,
        key="supports_web_search",
    )

