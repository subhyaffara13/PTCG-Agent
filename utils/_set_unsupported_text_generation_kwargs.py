
def _set_unsupported_text_generation_kwargs(model: str | None, unsupported_kwargs: list[str]) -> None:
    _UNSUPPORTED_TEXT_GENERATION_KWARGS.setdefault(model, []).extend(unsupported_kwargs)

