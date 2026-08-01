
def _init_socks5_connection(
    stream: NetworkStream,
    *,
    host: bytes,
    port: int,
    auth: tuple[bytes, bytes] | None = None,
) -> None:
    conn = socksio.socks5.SOCKS5Connection()

    # Auth method request
    auth_method = (
        socksio.socks5.SOCKS5AuthMethod.NO_AUTH_REQUIRED
        if auth is None
        else socksio.socks5.SOCKS5AuthMethod.USERNAME_PASSWORD
    )
    conn.send(socksio.socks5.SOCKS5AuthMethodsRequest([auth_method]))
    outgoing_bytes = conn.data_to_send()
    stream.write(outgoing_bytes)

    # Auth method response
    incoming_bytes = stream.read(max_bytes=4096)
    response = conn.receive_data(incoming_bytes)
    assert isinstance(response, socksio.socks5.SOCKS5AuthReply)
    if response.method != auth_method:
        requested = AUTH_METHODS.get(auth_method, "UNKNOWN")
        responded = AUTH_METHODS.get(response.method, "UNKNOWN")
        raise ProxyError(
            f"Requested {requested} from proxy server, but got {responded}."
        )

    if response.method == socksio.socks5.SOCKS5AuthMethod.USERNAME_PASSWORD:
        # Username/password request
        assert auth is not None
        username, password = auth
        conn.send(socksio.socks5.SOCKS5UsernamePasswordRequest(username, password))
        outgoing_bytes = conn.data_to_send()
        stream.write(outgoing_bytes)

        # Username/password response
        incoming_bytes = stream.read(max_bytes=4096)
        response = conn.receive_data(incoming_bytes)
        assert isinstance(response, socksio.socks5.SOCKS5UsernamePasswordReply)
        if not response.success:
            raise ProxyError("Invalid username/password")

    # Connect request
    conn.send(
        socksio.socks5.SOCKS5CommandRequest.from_address(
            socksio.socks5.SOCKS5Command.CONNECT, (host, port)
        )
    )
    outgoing_bytes = conn.data_to_send()
    stream.write(outgoing_bytes)

    # Connect response
    incoming_bytes = stream.read(max_bytes=4096)
    response = conn.receive_data(incoming_bytes)
    assert isinstance(response, socksio.socks5.SOCKS5Reply)
    if response.reply_code != socksio.socks5.SOCKS5ReplyCode.SUCCEEDED:
        reply_code = REPLY_CODES.get(response.reply_code, "UNKOWN")
        raise ProxyError(f"Proxy Server could not connect: {reply_code}.")

