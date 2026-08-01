
def _get_http_response_etag_or_last_modified(resp: Response) -> str | None:
    """
    Return either the ETag or Last-Modified header (or None if neither exists).
    The return value can be used in an If-Range header.
    """
    return resp.headers.get("etag", resp.headers.get("last-modified"))

