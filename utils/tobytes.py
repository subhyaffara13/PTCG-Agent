
def tobytes(s: str | bytes, encoding: str = "ascii", errors: str = "strict") -> bytes:
    if isinstance(s, str):
        return s.encode(encoding, errors)
    else:
        return bytes(s)

