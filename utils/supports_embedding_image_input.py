
def supports_embedding_image_input(
    model: str, custom_llm_provider: Optional[str] = None
) -> bool:
    """
    Check if the given model supports embedding image input and return a boolean value.
    """
    return _supports_factory(
        model=model,
        custom_llm_provider=custom_llm_provider,
        key="supports_embedding_image_input",
    )

