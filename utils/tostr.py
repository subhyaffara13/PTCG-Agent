
def tostr(s: str | bytes, encoding: str = "ascii", errors: str = "strict") -> str:
    if not isinstance(s, str):
        return s.decode(encoding, errors)
    else:
        return s

