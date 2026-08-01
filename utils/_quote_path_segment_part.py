
def _quote_path_segment_part(value: str) -> str:
    """Percent-encode `value` for use in a URI path segment.

    Considers characters not in `pchar` set from RFC 3986 §3.3 to be unsafe.
    https://datatracker.ietf.org/doc/html/rfc3986#section-3.3
    """
    # quote() already treats unreserved characters (letters, digits, and -._~)
    # as safe, so we only need to add sub-delims, ':', and '@'.
    # Notably, unlike the default `safe` for quote(), / is unsafe and must be quoted.
    return quote(value, safe="!$&'()*+,;=:@")

