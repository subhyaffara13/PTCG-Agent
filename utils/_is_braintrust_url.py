
def _is_braintrust_url(url: str) -> bool:
    """Check if URL is a Braintrust API URL."""
    if not isinstance(url, str):
        return False

    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()

    if not host:
        return False

    return (
        host == "braintrustdata.com"
        or host.endswith(".braintrustdata.com")
        or host == "braintrust.dev"
        or host.endswith(".braintrust.dev")
    )

