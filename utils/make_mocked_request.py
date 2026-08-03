from typing import Any

def make_mocked_request(
    method: str,
    path: str,
    headers: Any = None,
    *,
    match_info: Any = sentinel,
    version: HttpVersion = HttpVersion(1, 1),
    closing: bool = False,
    app: Any = None,
    writer: Any = sentinel,
    protocol: Any = sentinel,
    transport: Any = sentinel,
    payload: StreamReader = EMPTY_PAYLOAD,
    sslcontext: SSLContext | None = None,
    client_max_size: int = 1024**2,
    loop: Any = ...,
) -> Request:
    """Creates mocked web.Request testing purposes.

    Useful in unit tests, when spinning full web server is overkill or
    specific conditions and errors are hard to trigger.
    """
    task = mock.Mock()
    if loop is ...:
        # no loop passed, try to get the current one if
        # its is running as we need a real loop to create
        # executor jobs to be able to do testing
        # with a real executor
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = mock.Mock()
            loop.create_future.return_value = ()

    if version < HttpVersion(1, 1):
        closing = True

    if headers:
        headers = CIMultiDictProxy(CIMultiDict(headers))
        raw_hdrs = tuple(
            (k.encode("utf-8"), v.encode("utf-8")) for k, v in headers.items()
        )
    else:
        headers = CIMultiDictProxy(CIMultiDict())
        raw_hdrs = ()

    chunked = "chunked" in headers.get(hdrs.TRANSFER_ENCODING, "").lower()
    upgrade = headers.get(hdrs.CONNECTION, "").lower() == "upgrade" and bool(
        headers.get(hdrs.UPGRADE)
    )

    message = RawRequestMessage(
        method,
        path,
        version,
        headers,
        raw_hdrs,
        closing,
        None,
        upgrade,
        chunked,
        URL(path),
    )
    if app is None:
        app = _create_app_mock()

    if transport is sentinel:
        transport = _create_transport(sslcontext)

    if protocol is sentinel:
        protocol = mock.Mock()
        protocol.max_field_size = 8190
        protocol.max_line_length = 8190
        protocol.max_headers = 128
        protocol.transport = transport
        type(protocol).peername = mock.PropertyMock(
            return_value=transport.get_extra_info("peername")
        )
        type(protocol).sockname = mock.PropertyMock(
            return_value=transport.get_extra_info("sockname")
        )
        type(protocol).ssl_context = mock.PropertyMock(return_value=sslcontext)

    if writer is sentinel:
        writer = mock.Mock()
        writer.write_headers = make_mocked_coro(None)
        writer.write = make_mocked_coro(None)
        writer.write_eof = make_mocked_coro(None)
        writer.drain = make_mocked_coro(None)
        writer.transport = transport

    protocol.transport = transport
    protocol.writer = writer

    req = Request(
        message, payload, protocol, writer, task, loop, client_max_size=client_max_size
    )

    match_info = UrlMappingMatchInfo(
        {} if match_info is sentinel else match_info, mock.Mock()
    )
    match_info.add_app(app)
    req._match_info = match_info

    return req

