
def parse_headers(raw: str | None) -> dict[str, str]:
    """Parse an OTLP ``"k=v,k=v"`` header string into a dict."""
    headers: dict[str, str] = {}
    if not raw:
        return headers
    for pair in raw.split(","):
        if "=" in pair:
            key, _, value = pair.partition("=")
            headers[key.strip()] = value.strip()
    return headers

