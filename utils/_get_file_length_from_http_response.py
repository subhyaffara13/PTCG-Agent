
def _get_file_length_from_http_response(response: httpx.Response) -> int | None:
    """
    Get the length of the file from the HTTP response headers.

    This function extracts the file size from the HTTP response headers, either from the
    `Content-Range` or `Content-Length` header, if available (in that order).

    Args:
        response (`httpx.Response`):
            The HTTP response object.

    Returns:
        `int` or `None`: The length of the file in bytes, or None if not available.
    """

    # If HTTP response contains compressed body (e.g. gzip), the `Content-Length` header will
    # contain the length of the compressed body, not the uncompressed file size.
    # And at the start of transmission there's no way to know the uncompressed file size for gzip,
    # thus we return None in that case.
    content_encoding = response.headers.get("Content-Encoding", "identity").lower()
    if content_encoding != "identity":
        # gzip/br/deflate/zstd etc
        return None

    content_range = response.headers.get("Content-Range")
    if content_range is not None:
        return int(content_range.rsplit("/")[-1])

    content_length = response.headers.get("Content-Length")
    if content_length is not None:
        return int(content_length)

    return None

