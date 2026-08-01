
def _encode_without_bom(string: str, encoding: str) -> bytes:
    """Encode a string but remove the BOM."""
    return _remove_bom(string.encode(encoding), encoding)

