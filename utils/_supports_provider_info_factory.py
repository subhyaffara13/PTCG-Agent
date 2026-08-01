
def _supports_provider_info_factory(
    model: str, custom_llm_provider: Optional[str], key: str
) -> Optional[Literal[True]]:
    """
    Check if the given model supports a provider specific model info and return a boolean value.
    """

    provider_info = get_provider_info(
        model=model, custom_llm_provider=custom_llm_provider
    )

    if provider_info is not None and provider_info.get(key, False) is True:
        return True
    return None

