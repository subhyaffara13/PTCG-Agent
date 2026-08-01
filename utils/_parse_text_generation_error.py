
def _parse_text_generation_error(error: str | None, error_type: str | None) -> TextGenerationError:
    if error_type == "generation":
        return GenerationError(error)  # type: ignore
    if error_type == "incomplete_generation":
        return IncompleteGenerationError(error)  # type: ignore
    if error_type == "overloaded":
        return OverloadedError(error)  # type: ignore
    if error_type == "validation":
        return ValidationError(error)  # type: ignore
    return UnknownError(error)  # type: ignore

