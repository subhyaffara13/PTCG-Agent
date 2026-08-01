
def supports_pdf_input(model: str, custom_llm_provider: Optional[str] = None) -> bool:
    """Check if a given model supports pdf input in a chat completion call"""
    return _supports_factory(
        model=model, custom_llm_provider=custom_llm_provider, key="supports_pdf_input"
    )

