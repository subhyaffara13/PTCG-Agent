
def encode_url(url_str: str) -> "URL":
    """Parse unencoded URL."""
    cache: _InternalURLCache = {}
    host: str | None
    scheme, netloc, path, query, fragment = split_url(url_str)
    if not netloc:  # netloc
        host = ""
    else:
        if ":" in netloc or "@" in netloc or "[" in netloc:
            # Complex netloc
            username, password, host, port = split_netloc(netloc)
        else:
            username = password = port = None
            host = netloc
        if host is None:
            if scheme in SCHEME_REQUIRES_HOST:
                msg = (
                    "Invalid URL: host is required for "
                    f"absolute urls with the {scheme} scheme"
                )
                raise ValueError(msg)
            else:
                host = ""
        host = _encode_host(host, validate_host=False)
        # Remove brackets as host encoder adds back brackets for IPv6 addresses
        cache["raw_host"] = host[1:-1] if "[" in host else host
        cache["explicit_port"] = port
        if password is None and username is None:
            # Fast path for URLs without user, password
            netloc = host if port is None else f"{host}:{port}"
            cache["raw_user"] = None
            cache["raw_password"] = None
        else:
            raw_user = REQUOTER(username) if username else username
            raw_password = REQUOTER(password) if password else password
            netloc = make_netloc(raw_user, raw_password, host, port)
            cache["raw_user"] = raw_user
            cache["raw_password"] = raw_password

    if path:
        path = PATH_REQUOTER(path)
        if netloc and "." in path:
            path = normalize_path(path)
        elif not scheme and not netloc:
            path = _encode_relative_scheme_colon(path)
    if query:
        query = QUERY_REQUOTER(query)
    if fragment:
        fragment = FRAGMENT_REQUOTER(fragment)

    cache["scheme"] = scheme
    cache["raw_path"] = "/" if not path and netloc else path
    cache["raw_query_string"] = query
    cache["raw_fragment"] = fragment

    self = object.__new__(URL)
    self._scheme = scheme
    self._netloc = netloc
    self._path = path
    self._query = query
    self._fragment = fragment
    self._cache = cache
    return self

