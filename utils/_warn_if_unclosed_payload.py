
def _warn_if_unclosed_payload(payload: payload.Payload, stacklevel: int = 2) -> None:
    """Warn if the payload is not closed.

    Callers must check that the body is a Payload before calling this method.

    Args:
        payload: The payload to check
        stacklevel: Stack level for the warning (default 2 for direct callers)
    """
    if not payload.autoclose and not payload.consumed:
        warnings.warn(
            "The previous request body contains unclosed resources. "
            "Use await request.update_body() instead of setting request.body "
            "directly to properly close resources and avoid leaks.",
            ResourceWarning,
            stacklevel=stacklevel,
        )

