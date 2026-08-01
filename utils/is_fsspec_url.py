
def is_fsspec_url(url: FilePath | BaseBuffer) -> bool:
    """
    Returns true if the given URL looks like
    something fsspec can handle
    """
    return (
        isinstance(url, str)
        and bool(_FSSPEC_URL_PATTERN.match(url))
        and not url.startswith(("http://", "https://"))
    )

