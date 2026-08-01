
def _safe_get_request_headers(request: Optional[Request]) -> dict:
    """
    [Non-Blocking] Safely get the request headers.
    Caches the result on request.state to avoid re-creating dict(request.headers) per call.

    Warning: Callers must NOT mutate the returned dict — it is shared across
    all callers within the same request via the cache.
    """
    if request is None:
        return {}
    state = getattr(request, "state", None)
    cached = getattr(state, "_cached_headers", None)
    if isinstance(cached, dict):
        return cached
    if cached is not None:
        verbose_proxy_logger.debug(
            "Unexpected cached request headers type - {}".format(type(cached))
        )
    try:
        headers = dict(request.headers)
    except Exception as e:
        verbose_proxy_logger.debug(
            "Unexpected error reading request headers - {}".format(e)
        )
        headers = {}
    try:
        if state is not None:
            state._cached_headers = headers
    except Exception:
        pass  # request.state may not be available in all contexts
    return headers

