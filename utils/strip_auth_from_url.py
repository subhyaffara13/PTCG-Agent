
def strip_auth_from_url(url: URL) -> tuple[URL, BasicAuth | None]:
    """Remove user and password from URL if present and return BasicAuth object."""
    # Check raw_user and raw_password first as yarl is likely
    # to already have these values parsed from the netloc in the cache.
    if url.raw_user is None and url.raw_password is None:
        return url, None
    return url.with_user(None), _basic_auth_no_warn(url.user or "", url.password or "")

