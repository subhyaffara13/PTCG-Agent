
def _endpoint_host_and_path(endpoint: str | None) -> tuple[str | None, str]:
    """Return the lowercased host and stripped path prefix of a custom Hub 'endpoint'.

    E.g. 'https://hub.my-company.com' -> ('hub.my-company.com', '') and a self-hosted
    'http://localhost:8080/hf' -> ('localhost', 'hf'). Returns '(None, "")' when 'endpoint' is None.
    """
    if endpoint is None:
        return None, ""
    # Prefix '//' for scheme-less endpoints so 'urlsplit' populates 'netloc' instead of 'path'.
    parsed = urlsplit(endpoint if "://" in endpoint else "//" + endpoint)
    host = parsed.hostname.lower() if parsed.hostname else None
    return host, parsed.path.strip("/")

