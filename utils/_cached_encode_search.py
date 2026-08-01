
def _cached_encode_search(string: str, encoding: str) -> bytes:
    """A cached version of encode used for search pattern."""
    return _encode_without_bom(string, encoding)

