
def _remove_bom(encoded: bytes, encoding: str) -> bytes:
    """Remove the bom if given from a line."""
    if encoding not in UNICODE_BOMS:
        return encoded
    bom = UNICODE_BOMS[encoding]
    if encoded.startswith(bom):
        return encoded[len(bom) :]
    return encoded

