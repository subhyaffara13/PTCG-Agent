
def _get_unsupported_text_generation_kwargs(model: str | None) -> list[str]:
    return _UNSUPPORTED_TEXT_GENERATION_KWARGS.get(model, [])

