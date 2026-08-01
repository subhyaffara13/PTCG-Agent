
def start_wsgi_server(
        port: int,
        addr: str = '0.0.0.0',
        registry: Collector = REGISTRY,
        certfile: Optional[str] = None,
        keyfile: Optional[str] = None,
        client_cafile: Optional[str] = None,
        client_capath: Optional[str] = None,
        protocol: int = ssl.PROTOCOL_TLS_SERVER,
        client_auth_required: bool = False,
) -> Tuple[WSGIServer, threading.Thread]:
    """Starts a WSGI server for prometheus metrics as a daemon thread."""

    class TmpServer(ThreadingWSGIServer):
        """Copy of ThreadingWSGIServer to update address_family locally"""

    TmpServer.address_family, addr = _get_best_family(addr, port)
    app = make_wsgi_app(registry)
    httpd = make_server(addr, port, app, TmpServer, handler_class=_SilentHandler)
    if certfile and keyfile:
        context = _get_ssl_ctx(certfile, keyfile, protocol, client_cafile, client_capath, client_auth_required)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    t = threading.Thread(target=httpd.serve_forever)
    t.daemon = True
    t.start()

    return httpd, t

