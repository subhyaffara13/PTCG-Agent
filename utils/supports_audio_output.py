
def supports_audio_output(
    model: str, custom_llm_provider: Optional[str] = None
) -> bool:
    """Check if a given model supports audio output in a chat completion call"""
    return _supports_factory(
        model=model, custom_llm_provider=custom_llm_provider, key="supports_audio_input"
    )

