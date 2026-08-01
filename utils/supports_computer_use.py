
def supports_computer_use(
    model: str, custom_llm_provider: Optional[str] = None
) -> bool:
    """
    Check if the given model supports computer use and return a boolean value.

    Parameters:
    model (str): The model name to be checked.
    custom_llm_provider (Optional[str]): The provider to be checked.

    Returns:
    bool: True if the model supports computer use, False otherwise.

    Raises:
    Exception: If the given model is not found or there's an error in retrieval.
    """
    return _supports_factory(
        model=model,
        custom_llm_provider=custom_llm_provider,
        key="supports_computer_use",
    )

