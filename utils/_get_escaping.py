
def _get_escaping(accept_header: List[str]) -> str:
    """Return the escaping scheme from the Accept header.

    If no escaping scheme is specified or the scheme is not one of the allowed
    strings, defaults to UNDERSCORES."""

    for tok in accept_header:
        if '=' not in tok:
            continue
        key, value = tok.strip().split('=', 1)
        if key != 'escaping':
            continue
        if value == openmetrics.ALLOWUTF8:
            return openmetrics.ALLOWUTF8
        elif value == openmetrics.UNDERSCORES:
            return openmetrics.UNDERSCORES
        elif value == openmetrics.DOTS:
            return openmetrics.DOTS
        elif value == openmetrics.VALUES:
            return openmetrics.VALUES
        else:
            return openmetrics.UNDERSCORES
    return openmetrics.UNDERSCORES

