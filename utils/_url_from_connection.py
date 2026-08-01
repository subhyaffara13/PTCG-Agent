
def _url_from_connection(
    conn: HTTPConnection | HTTPSConnection, path: str | None = None
) -> str:
    """Returns the URL from a given connection. This is mainly used for testing and logging."""

    scheme = "https" if isinstance(conn, HTTPSConnection) else "http"

    return Url(scheme=scheme, host=conn.host, port=conn.port, path=path).url


def _url_from_connection(
    conn: HTTPConnection | HTTPSConnection, path: str | None = None
) -> str:
    """Returns the URL from a given connection. This is mainly used for testing and logging."""

    scheme = "https" if isinstance(conn, HTTPSConnection) else "http"

    return Url(scheme=scheme, host=conn.host, port=conn.port, path=path).url

