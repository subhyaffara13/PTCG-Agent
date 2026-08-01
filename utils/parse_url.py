
def parse_url(url):
    if not (
        url.startswith("redis://")
        or url.startswith("rediss://")
        or url.startswith("unix://")
    ):
        raise ValueError(
            "Redis URL must specify one of the following "
            "schemes (redis://, rediss://, unix://)"
        )

    url = urlparse(url)
    kwargs = {}

    for name, value in parse_qs(url.query).items():
        if value and len(value) > 0:
            value = unquote(value[0])
            parser = URL_QUERY_ARGUMENT_PARSERS.get(name)
            if parser:
                try:
                    kwargs[name] = parser(value)
                except (TypeError, ValueError):
                    raise ValueError(f"Invalid value for '{name}' in connection URL.")
            else:
                kwargs[name] = value

    if url.username:
        kwargs["username"] = unquote(url.username)
    if url.password:
        kwargs["password"] = unquote(url.password)

    # We only support redis://, rediss:// and unix:// schemes.
    if url.scheme == "unix":
        if url.path:
            kwargs["path"] = unquote(url.path)
        kwargs["connection_class"] = UnixDomainSocketConnection

    else:  # implied:  url.scheme in ("redis", "rediss"):
        if url.hostname:
            kwargs["host"] = unquote(url.hostname)
        if url.port:
            kwargs["port"] = int(url.port)

        # If there's a path argument, use it as the db argument if a
        # querystring value wasn't specified
        if url.path and "db" not in kwargs:
            try:
                kwargs["db"] = int(unquote(url.path).replace("/", ""))
            except (AttributeError, ValueError):
                pass

        if url.scheme == "rediss":
            kwargs["connection_class"] = SSLConnection

    return kwargs


def parse_url(url: str) -> Url:
    """
    Given a url, return a parsed :class:`.Url` namedtuple. Best-effort is
    performed to parse incomplete urls. Fields not provided will be None.
    This parser is RFC 3986 and RFC 6874 compliant.

    The parser logic and helper functions are based heavily on
    work done in the ``rfc3986`` module.

    :param str url: URL to parse into a :class:`.Url` namedtuple.

    Partly backwards-compatible with :mod:`urllib.parse`.

    Example:

    .. code-block:: python

        import urllib3

        print( urllib3.util.parse_url('http://google.com/mail/'))
        # Url(scheme='http', host='google.com', port=None, path='/mail/', ...)

        print( urllib3.util.parse_url('google.com:80'))
        # Url(scheme=None, host='google.com', port=80, path=None, ...)

        print( urllib3.util.parse_url('/foo?bar'))
        # Url(scheme=None, host=None, port=None, path='/foo', query='bar', ...)
    """
    if not url:
        # Empty
        return Url()

    source_url = url
    if not _SCHEME_RE.search(url):
        url = "//" + url

    scheme: str | None
    authority: str | None
    auth: str | None
    host: str | None
    port: str | None
    port_int: int | None
    path: str | None
    query: str | None
    fragment: str | None

    try:
        scheme, authority, path, query, fragment = _URI_RE.match(url).groups()  # type: ignore[union-attr]
        normalize_uri = scheme is None or scheme.lower() in _NORMALIZABLE_SCHEMES

        if scheme:
            scheme = scheme.lower()

        if authority:
            auth, _, host_port = authority.rpartition("@")
            auth = auth or None
            host, port = _HOST_PORT_RE.match(host_port).groups()  # type: ignore[union-attr]
            if auth and normalize_uri:
                auth = _encode_invalid_chars(auth, _USERINFO_CHARS)
            if port == "":
                port = None
        else:
            auth, host, port = None, None, None

        if port is not None:
            port_int = int(port)
            if not (0 <= port_int <= 65535):
                raise LocationParseError(url)
        else:
            port_int = None

        host = _normalize_host(host, scheme)

        if normalize_uri and path:
            path = _remove_path_dot_segments(path)
            path = _encode_invalid_chars(path, _PATH_CHARS)
        if normalize_uri and query:
            query = _encode_invalid_chars(query, _QUERY_CHARS)
        if normalize_uri and fragment:
            fragment = _encode_invalid_chars(fragment, _FRAGMENT_CHARS)

    except (ValueError, AttributeError) as e:
        raise LocationParseError(source_url) from e

    # For the sake of backwards compatibility we put empty
    # string values for path if there are any defined values
    # beyond the path in the URL.
    # TODO: Remove this when we break backwards compatibility.
    if not path:
        if query is not None or fragment is not None:
            path = ""
        else:
            path = None

    return Url(
        scheme=scheme,
        auth=auth,
        host=host,
        port=port_int,
        path=path,
        query=query,
        fragment=fragment,
    )


def parse_url(url: str) -> ConnectKwargs:
    parsed: ParseResult = urlparse(url)
    kwargs: ConnectKwargs = {}

    for name, value_list in parse_qs(parsed.query).items():
        if value_list and len(value_list) > 0:
            value = unquote(value_list[0])
            parser = URL_QUERY_ARGUMENT_PARSERS.get(name)
            if parser:
                try:
                    kwargs[name] = parser(value)
                except (TypeError, ValueError):
                    raise ValueError(f"Invalid value for '{name}' in connection URL.")
            else:
                kwargs[name] = value

    if parsed.username:
        kwargs["username"] = unquote(parsed.username)
    if parsed.password:
        kwargs["password"] = unquote(parsed.password)

    # We only support redis://, rediss:// and unix:// schemes.
    if parsed.scheme == "unix":
        if parsed.path:
            kwargs["path"] = unquote(parsed.path)
        kwargs["connection_class"] = UnixDomainSocketConnection

    elif parsed.scheme in ("redis", "rediss"):
        if parsed.hostname:
            kwargs["host"] = unquote(parsed.hostname)
        if parsed.port:
            kwargs["port"] = int(parsed.port)

        # If there's a path argument, use it as the db argument if a
        # querystring value wasn't specified
        if parsed.path and "db" not in kwargs:
            try:
                kwargs["db"] = int(unquote(parsed.path).replace("/", ""))
            except (AttributeError, ValueError):
                pass

        if parsed.scheme == "rediss":
            kwargs["connection_class"] = SSLConnection

    else:
        valid_schemes = "redis://, rediss://, unix://"
        raise ValueError(
            f"Redis URL must specify one of the following schemes ({valid_schemes})"
        )

    return kwargs


def parse_url(url: str) -> Url:
    """
    Given a url, return a parsed :class:`.Url` namedtuple. Best-effort is
    performed to parse incomplete urls. Fields not provided will be None.
    This parser is RFC 3986 and RFC 6874 compliant.

    The parser logic and helper functions are based heavily on
    work done in the ``rfc3986`` module.

    :param str url: URL to parse into a :class:`.Url` namedtuple.

    Partly backwards-compatible with :mod:`urllib.parse`.

    Example:

    .. code-block:: python

        from pip._vendor import urllib3

        print( urllib3.util.parse_url('http://google.com/mail/'))
        # Url(scheme='http', host='google.com', port=None, path='/mail/', ...)

        print( urllib3.util.parse_url('google.com:80'))
        # Url(scheme=None, host='google.com', port=80, path=None, ...)

        print( urllib3.util.parse_url('/foo?bar'))
        # Url(scheme=None, host=None, port=None, path='/foo', query='bar', ...)
    """
    if not url:
        # Empty
        return Url()

    source_url = url
    if not _SCHEME_RE.search(url):
        url = "//" + url

    scheme: str | None
    authority: str | None
    auth: str | None
    host: str | None
    port: str | None
    port_int: int | None
    path: str | None
    query: str | None
    fragment: str | None

    try:
        scheme, authority, path, query, fragment = _URI_RE.match(url).groups()  # type: ignore[union-attr]
        normalize_uri = scheme is None or scheme.lower() in _NORMALIZABLE_SCHEMES

        if scheme:
            scheme = scheme.lower()

        if authority:
            auth, _, host_port = authority.rpartition("@")
            auth = auth or None
            host, port = _HOST_PORT_RE.match(host_port).groups()  # type: ignore[union-attr]
            if auth and normalize_uri:
                auth = _encode_invalid_chars(auth, _USERINFO_CHARS)
            if port == "":
                port = None
        else:
            auth, host, port = None, None, None

        if port is not None:
            port_int = int(port)
            if not (0 <= port_int <= 65535):
                raise LocationParseError(url)
        else:
            port_int = None

        host = _normalize_host(host, scheme)

        if normalize_uri and path:
            path = _remove_path_dot_segments(path)
            path = _encode_invalid_chars(path, _PATH_CHARS)
        if normalize_uri and query:
            query = _encode_invalid_chars(query, _QUERY_CHARS)
        if normalize_uri and fragment:
            fragment = _encode_invalid_chars(fragment, _FRAGMENT_CHARS)

    except (ValueError, AttributeError) as e:
        raise LocationParseError(source_url) from e

    # For the sake of backwards compatibility we put empty
    # string values for path if there are any defined values
    # beyond the path in the URL.
    # TODO: Remove this when we break backwards compatibility.
    if not path:
        if query is not None or fragment is not None:
            path = ""
        else:
            path = None

    return Url(
        scheme=scheme,
        auth=auth,
        host=host,
        port=port_int,
        path=path,
        query=query,
        fragment=fragment,
    )

