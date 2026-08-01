
def _url_name(url: str | None) -> str | None:
    if not url:
        return None
    url_path = urlparse(url).path
    return url_path.rsplit("/", 1)[-1]


def _url_name(url: str | None) -> str | None:
    if not url:
        return None
    url_path = urlparse(url).path
    return url_path.rsplit("/", 1)[-1]

