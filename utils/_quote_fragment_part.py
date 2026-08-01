
def _quote_fragment_part(value: str) -> str:
    """Percent-encode `value` for use in a URI fragment.

    Considers characters not in `fragment` set from RFC 3986 §3.5 to be unsafe.
    https://datatracker.ietf.org/doc/html/rfc3986#section-3.5
    """
    return quote(value, safe="!$&'()*+,;=:@/?")

