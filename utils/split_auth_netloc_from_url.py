
def split_auth_netloc_from_url(
    url: str,
) -> tuple[str, str, tuple[str | None, str | None]]:
    """
    Parse a url into separate netloc, auth, and url with no auth.

    Returns: (url_without_auth, netloc, (username, password))
    """
    url_without_auth, (netloc, auth) = _transform_url(url, _get_netloc)
    return url_without_auth, netloc, auth

