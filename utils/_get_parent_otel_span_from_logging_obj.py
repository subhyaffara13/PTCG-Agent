
def _get_parent_otel_span_from_logging_obj(
    logging_obj: Optional[LiteLLMLoggingObject] = None,
) -> Optional[Span]:
    """
    Extract the parent OTEL span from the logging object using existing helper.

    Args:
        logging_obj: The LiteLLM logging object containing model call details

    Returns:
        The parent OTEL span if found, None otherwise
    """
    try:
        if logging_obj is None or not hasattr(logging_obj, "model_call_details"):
            return None

        # Reuse existing function by passing model_call_details as kwargs
        from litellm.litellm_core_utils.core_helpers import (
            _get_parent_otel_span_from_kwargs,
        )

        return _get_parent_otel_span_from_kwargs(logging_obj.model_call_details)

    except Exception as e:
        verbose_logger.exception(
            f"Error in _get_parent_otel_span_from_logging_obj: {str(e)}"
        )
        return None

