
def _set_usage_on_logging_obj(
    kwargs: Dict[str, Any],
    prompt_tokens: int,
    completion_tokens: int,
) -> None:
    """
    Set usage on litellm_logging_obj for standard logging payload.

    Args:
        kwargs: The kwargs dict containing litellm_logging_obj
        prompt_tokens: Number of input tokens
        completion_tokens: Number of output tokens
    """
    litellm_logging_obj = kwargs.get("litellm_logging_obj")
    if litellm_logging_obj is not None:
        usage = litellm.Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
        litellm_logging_obj.model_call_details["usage"] = usage

