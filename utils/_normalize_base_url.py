import re

def _normalize_base_url(base_url: str | httpx.URL) -> httpx.URL:
    url = httpx.URL(base_url)
    path = url.path.rstrip("/")
    responses_match = re.search(r"/responses(?:/.*)?$", path)
    if responses_match is not None:
        path = path[: responses_match.start()]

    return url.copy_with(path=path or "/")


def _normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")

