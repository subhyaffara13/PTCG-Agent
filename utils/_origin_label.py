
def _origin_label(scheme: str, netloc: str) -> str:
    """Human-readable origin for error messages (scheme + host[:port])."""
    return f"{scheme}://{netloc}" if netloc else f"{scheme}://"

