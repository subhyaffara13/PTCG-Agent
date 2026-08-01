
def _wsgi_decoding_dance(s: str) -> str:
    return s.encode("latin1").decode(errors="replace")

