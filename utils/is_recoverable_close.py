
def is_recoverable_close(code: int) -> bool:
    """Return ``True`` if the WebSocket close *code* is worth retrying."""
    return code in _RECOVERABLE_CLOSE_CODES

