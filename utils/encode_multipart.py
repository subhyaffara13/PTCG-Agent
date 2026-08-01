
def encode_multipart(
    values: t.Mapping[str, t.Any], boundary: str | None = None
) -> tuple[str, bytes]:
    """Like `stream_encode_multipart` but returns a tuple in the form
    (``boundary``, ``data``) where data is bytes.

    .. versionchanged:: 3.0
        The ``charset`` parameter was removed.
    """
    stream, length, boundary = stream_encode_multipart(
        values, use_tempfile=False, boundary=boundary
    )
    return boundary, stream.read()

