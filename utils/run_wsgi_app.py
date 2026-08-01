
def run_wsgi_app(
    app: WSGIApplication, environ: WSGIEnvironment, buffered: bool = False
) -> tuple[t.Iterable[bytes], str, Headers]:
    """Return a tuple in the form (app_iter, status, headers) of the
    application output.  This works best if you pass it an application that
    returns an iterator all the time.

    Sometimes applications may use the `write()` callable returned
    by the `start_response` function.  This tries to resolve such edge
    cases automatically.  But if you don't get the expected output you
    should set `buffered` to `True` which enforces buffering.

    If passed an invalid WSGI application the behavior of this function is
    undefined.  Never pass non-conforming WSGI applications to this function.

    :param app: the application to execute.
    :param buffered: set to `True` to enforce buffering.
    :return: tuple in the form ``(app_iter, status, headers)``
    """
    # Copy environ to ensure any mutations by the app (ProxyFix, for
    # example) don't affect subsequent requests (such as redirects).
    environ = _get_environ(environ).copy()
    status: str
    response: tuple[str, list[tuple[str, str]]] | None = None
    buffer: list[bytes] = []

    def start_response(status, headers, exc_info=None):  # type: ignore
        nonlocal response

        if exc_info:
            try:
                raise exc_info[1].with_traceback(exc_info[2])
            finally:
                exc_info = None

        response = (status, headers)
        return buffer.append

    app_rv = app(environ, start_response)
    close_func = getattr(app_rv, "close", None)
    app_iter: t.Iterable[bytes] = iter(app_rv)

    # when buffering we emit the close call early and convert the
    # application iterator into a regular list
    if buffered:
        try:
            app_iter = list(app_iter)
        finally:
            if close_func is not None:
                close_func()

    # otherwise we iterate the application iter until we have a response, chain
    # the already received data with the already collected data and wrap it in
    # a new `ClosingIterator` if we need to restore a `close` callable from the
    # original return value.
    else:
        for item in app_iter:
            buffer.append(item)

            if response is not None:
                break

        if buffer:
            app_iter = chain(buffer, app_iter)

        if close_func is not None and app_iter is not app_rv:
            app_iter = ClosingIterator(app_iter, close_func)

    status, headers = response  # type: ignore
    return app_iter, status, Headers(headers)

