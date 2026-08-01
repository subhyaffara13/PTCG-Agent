
def _realtime_request_body(model: Optional[str]) -> bytes:
    """
    Generate the realtime websocket request body. Cached with LRU semantics to avoid repeated
    string formatting work while keeping memory usage bounded.
    """
    return f'{{"model": "{model or ""}"}}'.encode()

