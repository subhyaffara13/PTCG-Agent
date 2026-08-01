
def get_content_length(environ: WSGIEnvironment) -> int | None:
    """Return the ``Content-Length`` header value as an int. If the header is not given
    or the ``Transfer-Encoding`` header is ``chunked``, ``None`` is returned to indicate
    a streaming request. If the value is not an integer, or negative, 0 is returned.

    :param environ: The WSGI environ to get the content length from.

    .. versionadded:: 0.9
    """
    return _sansio_utils.get_content_length(
        http_content_length=environ.get("CONTENT_LENGTH"),
        http_transfer_encoding=environ.get("HTTP_TRANSFER_ENCODING"),
    )


def get_content_length(
    http_content_length: str | None = None,
    http_transfer_encoding: str | None = None,
) -> int | None:
    """Return the ``Content-Length`` header value as an int. If the header is not given
    or the ``Transfer-Encoding`` header is ``chunked``, ``None`` is returned to indicate
    a streaming request. If the value is not an integer, or negative, 0 is returned.

    :param http_content_length: The Content-Length HTTP header.
    :param http_transfer_encoding: The Transfer-Encoding HTTP header.

    .. versionadded:: 2.2
    """
    if (
        http_transfer_encoding is not None
        and "chunked" in parse_set_header(http_transfer_encoding)
    ) or http_content_length is None:
        return None

    try:
        return max(0, _plain_int(http_content_length))
    except ValueError:
        return 0

