
def make_server(
    host: str,
    port: int,
    app: WSGIApplication,
    threaded: bool = False,
    processes: int = 1,
    request_handler: type[WSGIRequestHandler] | None = None,
    passthrough_errors: bool = False,
    ssl_context: _TSSLContextArg | None = None,
    fd: int | None = None,
) -> BaseWSGIServer:
    """Create an appropriate WSGI server instance based on the value of
    ``threaded`` and ``processes``.

    This is called from :func:`run_simple`, but can be used separately
    to have access to the server object, such as to run it in a separate
    thread.

    See :func:`run_simple` for parameter docs.
    """
    if threaded and processes > 1:
        raise ValueError("Cannot have a multi-thread and multi-process server.")

    if threaded:
        return ThreadedWSGIServer(
            host, port, app, request_handler, passthrough_errors, ssl_context, fd=fd
        )

    if processes > 1:
        return ForkingWSGIServer(
            host,
            port,
            app,
            processes,
            request_handler,
            passthrough_errors,
            ssl_context,
            fd=fd,
        )

    return BaseWSGIServer(
        host, port, app, request_handler, passthrough_errors, ssl_context, fd=fd
    )

