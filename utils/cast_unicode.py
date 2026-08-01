
def cast_unicode(s: str | bytes, encoding: str = "utf-8") -> str:
    if isinstance(s, bytes):
        return s.decode(encoding, "replace")
    return s

