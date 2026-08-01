
def supports_vision(model: str, custom_llm_provider: Optional[str] = None) -> bool:
    """
    Check if the given model supports vision and return a boolean value.

    Parameters:
    model (str): The model name to be checked.
    custom_llm_provider (Optional[str]): The provider to be checked.

    Returns:
    bool: True if the model supports vision, False otherwise.
    """
    return _supports_factory(
        model=model,
        custom_llm_provider=custom_llm_provider,
        key="supports_vision",
    )

