
def _wsgi_encoding_dance(s: str) -> str:
    return s.encode().decode("latin1")

