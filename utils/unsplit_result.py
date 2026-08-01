
def unsplit_result(
    scheme: str, netloc: str, url: str, query: str, fragment: str
) -> str:
    """Unsplit a URL without any normalization."""
    if netloc or (scheme and scheme in USES_AUTHORITY) or url[:2] == "//":
        if url and url[:1] != "/":
            url = f"{scheme}://{netloc}/{url}" if scheme else f"{scheme}:{url}"
        else:
            url = f"{scheme}://{netloc}{url}" if scheme else f"//{netloc}{url}"
    elif scheme:
        url = f"{scheme}:{url}"
    if query:
        url = f"{url}?{query}"
    return f"{url}#{fragment}" if fragment else url

