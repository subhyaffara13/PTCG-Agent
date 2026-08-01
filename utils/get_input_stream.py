
def get_input_stream(
    environ: WSGIEnvironment,
    safe_fallback: bool = True,
    max_content_length: int | None = None,
) -> t.IO[bytes]:
    """Return the WSGI input stream, wrapped so that it may be read safely without going
    past the ``Content-Length`` header value or ``max_content_length``.

    If ``Content-Length`` exceeds ``max_content_length``, a
    :exc:`RequestEntityTooLarge`` ``413 Content Too Large`` error is raised.

    If the WSGI server sets ``environ["wsgi.input_terminated"]``, it indicates that the
    server handles terminating the stream, so it is safe to read directly. For example,
    a server that knows how to handle chunked requests safely would set this.

    If ``max_content_length`` is set, it can be enforced on streams if
    ``wsgi.input_terminated`` is set. Otherwise, an empty stream is returned unless the
    user explicitly disables this safe fallback.

    If the limit is reached before the underlying stream is exhausted (such as a file
    that is too large, or an infinite stream), the remaining contents of the stream
    cannot be read safely. Depending on how the server handles this, clients may show a
    "connection reset" failure instead of seeing the 413 response.

    :param environ: The WSGI environ containing the stream.
    :param safe_fallback: Return an empty stream when ``Content-Length`` is not set.
        Disabling this allows infinite streams, which can be a denial-of-service risk.
    :param max_content_length: The maximum length that content-length or streaming
        requests may not exceed.

    .. versionchanged:: 2.3.2
        ``max_content_length`` is only applied to streaming requests if the server sets
        ``wsgi.input_terminated``.

    .. versionchanged:: 2.3
        Check ``max_content_length`` and raise an error if it is exceeded.

    .. versionadded:: 0.9
    """
    stream = t.cast(t.IO[bytes], environ["wsgi.input"])
    content_length = get_content_length(environ)

    if content_length is not None and max_content_length is not None:
        if content_length > max_content_length:
            raise RequestEntityTooLarge()

    # A WSGI server can set this to indicate that it terminates the input stream. In
    # that case the stream is safe without wrapping, or can enforce a max length.
    if "wsgi.input_terminated" in environ:
        if max_content_length is not None:
            # If this is moved above, it can cause the stream to hang if a read attempt
            # is made when the client sends no data. For example, the development server
            # does not handle buffering except for chunked encoding.
            return t.cast(
                t.IO[bytes], LimitedStream(stream, max_content_length, is_max=True)
            )

        return stream

    # No limit given, return an empty stream unless the user explicitly allows the
    # potentially infinite stream. An infinite stream is dangerous if it's not expected,
    # as it can tie up a worker indefinitely.
    if content_length is None:
        return io.BytesIO() if safe_fallback else stream

    return t.cast(t.IO[bytes], LimitedStream(stream, content_length))

