
def _quote_query_part(value: str) -> str:
    """Percent-encode `value` for use in a URI query string.

    Considers &, = and characters not in `query` set from RFC 3986 §3.4 to be unsafe.
    https://datatracker.ietf.org/doc/html/rfc3986#section-3.4
    """
    return quote(value, safe="!$'()*+,;:@/?")

