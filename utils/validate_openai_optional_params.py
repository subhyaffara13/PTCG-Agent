
def validate_openai_optional_params(
    stop: Optional[Union[str, List[str]]] = None, **kwargs
) -> Optional[Union[str, List[str]]]:
    """
    Validates and fixes OpenAI optional parameters.

    Args:
        stop: Stop sequences (string or list of strings)
        **kwargs: Additional optional parameters

    Returns:
        Validated stop parameter (truncated to 4 elements if needed)
    """
    if (
        stop is not None
        and isinstance(stop, list)
        and not litellm.disable_stop_sequence_limit
    ):
        # Truncate to 4 elements if more are provided as openai only supports up to 4 stop sequences
        if len(stop) > 4:
            stop = stop[:4]

    return stop

