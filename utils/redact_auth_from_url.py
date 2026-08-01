
def redact_auth_from_url(url: str) -> str:
    """Replace the password in a given url with ****."""
    return _transform_url(url, _redact_netloc)[0]

