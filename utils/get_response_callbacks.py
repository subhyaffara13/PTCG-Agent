
def get_response_callbacks(
    user_protocol: Optional[int],
    legacy_responses: bool,
) -> dict[str, Callable[..., Any]]:
    """Return the merged callback dict for the given (protocol, legacy)
    combination.

    ``user_protocol`` is the value the user supplied to the client
    constructor (``None`` means "not specified"). ``legacy_responses``
    defaults to ``True`` and selects today's RESP2-style Python shapes
    even when the wire protocol is RESP3.

    Callers wrap the returned dict in ``CaseInsensitiveDict``.
    """
    callbacks: dict[str, Callable[..., Any]] = dict(_RedisCallbacks)
    if legacy_responses:
        if user_protocol is None:
            callbacks.update(_RedisCallbacksRESP3toRESP2Legacy)
        elif user_protocol in (3, "3"):
            callbacks.update(_RedisCallbacksRESP3)
        else:
            callbacks.update(_RedisCallbacksRESP2)
    else:
        if user_protocol is None or user_protocol in (3, "3"):
            callbacks.update(_RedisCallbacksRESP3Unified)
        else:
            callbacks.update(_RedisCallbacksRESP2Unified)
    return callbacks

