
def _create_transport(sslcontext: SSLContext | None = None) -> mock.Mock:
    transport = mock.Mock()

    def get_extra_info(key: str) -> SSLContext | tuple[str, int] | None:
        if key == "sslcontext":
            return sslcontext
        return ("127.0.0.1", 80) if key == "sockname" else None

    transport.get_extra_info.side_effect = get_extra_info
    return transport

