
def _get_session_id_for_spend_log(
    kwargs: dict,
    standard_logging_payload: Optional[StandardLoggingPayload],
) -> str:
    """
    Get the session id for the spend log.

    This ensures each spend log is associated with a unique session id.

    """
    from litellm._uuid import uuid

    if (
        standard_logging_payload is not None
        and standard_logging_payload.get("trace_id") is not None
    ):
        return str(standard_logging_payload.get("trace_id"))

    # Users can dynamically set the trace_id for each request by passing `litellm_trace_id` in kwargs
    if kwargs.get("litellm_trace_id") is not None:
        return str(kwargs.get("litellm_trace_id"))

    # Ensure we always have a session id, if none is provided
    return str(uuid.uuid4())

