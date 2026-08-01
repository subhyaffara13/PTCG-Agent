
def include_request_headers(
    headers: list[tuple[bytes, bytes]],
    *,
    url: "URL",
    content: None | bytes | typing.Iterable[bytes] | typing.AsyncIterable[bytes],
) -> list[tuple[bytes, bytes]]:
    headers_set = set(k.lower() for k, v in headers)

    if b"host" not in headers_set:
        default_port = DEFAULT_PORTS.get(url.scheme)
        if url.port is None or url.port == default_port:
            header_value = url.host
        else:
            header_value = b"%b:%d" % (url.host, url.port)
        headers = [(b"Host", header_value)] + headers

    if (
        content is not None
        and b"content-length" not in headers_set
        and b"transfer-encoding" not in headers_set
    ):
        if isinstance(content, bytes):
            content_length = str(len(content)).encode("ascii")
            headers += [(b"Content-Length", content_length)]
        else:
            headers += [(b"Transfer-Encoding", b"chunked")]  # pragma: nocover

    return headers

