
def _url_from_pool(
    pool: HTTPConnectionPool | HTTPSConnectionPool, path: str | None = None
) -> str:
    """Returns the URL from a given connection pool. This is mainly used for testing and logging."""
    return Url(scheme=pool.scheme, host=pool.host, port=pool.port, path=path).url


def _url_from_pool(
    pool: HTTPConnectionPool | HTTPSConnectionPool, path: str | None = None
) -> str:
    """Returns the URL from a given connection pool. This is mainly used for testing and logging."""
    return Url(scheme=pool.scheme, host=pool.host, port=pool.port, path=path).url

