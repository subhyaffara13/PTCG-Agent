
def build_pre_encoded_url(
    scheme: str,
    authority: str,
    user: str | None,
    password: str | None,
    host: str,
    port: int | None,
    path: str,
    query_string: str,
    fragment: str,
) -> "URL":
    """Build a pre-encoded URL from parts."""
    self = object.__new__(URL)
    self._scheme = scheme
    if authority:
        self._netloc = authority
    elif host:
        if port is not None:
            port = None if port == DEFAULT_PORTS.get(scheme) else port
        if user is None and password is None:
            self._netloc = host if port is None else f"{host}:{port}"
        else:
            self._netloc = make_netloc(user, password, host, port)
    else:
        self._netloc = ""
    self._path = path
    self._query = query_string
    self._fragment = fragment
    self._cache = {}
    return self

