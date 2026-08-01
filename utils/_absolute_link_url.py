
def _absolute_link_url(base_url: str, url: str) -> str:
    """
    A faster implementation of urllib.parse.urljoin with a shortcut
    for absolute http/https URLs.
    """
    if url.startswith(("https://", "http://")):
        return url
    else:
        return urllib.parse.urljoin(base_url, url)

