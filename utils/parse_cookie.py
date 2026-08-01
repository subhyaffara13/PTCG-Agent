
def parse_cookie(
    header: WSGIEnvironment | str | None,
    cls: type[ds.MultiDict[str, str]] | None = None,
) -> ds.MultiDict[str, str]:
    """Parse a cookie from a string or WSGI environ.

    The same key can be provided multiple times, the values are stored
    in-order. The default :class:`MultiDict` will have the first value
    first, and all values can be retrieved with
    :meth:`MultiDict.getlist`.

    :param header: The cookie header as a string, or a WSGI environ dict
        with a ``HTTP_COOKIE`` key.
    :param cls: A dict-like class to store the parsed cookies in.
        Defaults to :class:`MultiDict`.

    .. versionchanged:: 3.0
        Passing bytes, and the ``charset`` and ``errors`` parameters, were removed.

    .. versionchanged:: 1.0
        Returns a :class:`MultiDict` instead of a ``TypeConversionDict``.

    .. versionchanged:: 0.5
        Returns a :class:`TypeConversionDict` instead of a regular dict. The ``cls``
        parameter was added.
    """
    if isinstance(header, dict):
        cookie = header.get("HTTP_COOKIE")
    else:
        cookie = header

    if cookie:
        cookie = cookie.encode("latin1").decode()

    return _sansio_http.parse_cookie(cookie=cookie, cls=cls)


def parse_cookie(
    cookie: str | None = None,
    cls: type[ds.MultiDict[str, str]] | None = None,
) -> ds.MultiDict[str, str]:
    """Parse a cookie from a string.

    The same key can be provided multiple times, the values are stored
    in-order. The default :class:`MultiDict` will have the first value
    first, and all values can be retrieved with
    :meth:`MultiDict.getlist`.

    :param cookie: The cookie header as a string.
    :param cls: A dict-like class to store the parsed cookies in.
        Defaults to :class:`MultiDict`.

    .. versionchanged:: 3.0
        Passing bytes, and the ``charset`` and ``errors`` parameters, were removed.

    .. versionadded:: 2.2
    """
    if cls is None:
        cls = t.cast("type[ds.MultiDict[str, str]]", ds.MultiDict)

    if not cookie:
        return cls()

    cookie = f"{cookie};"
    out = []

    for ck, cv in _cookie_re.findall(cookie):
        ck = ck.strip()
        cv = cv.strip()

        if not ck:
            continue

        if len(cv) >= 2 and cv[0] == cv[-1] == '"':
            # Work with bytes here, since a UTF-8 character could be multiple bytes.
            cv = _cookie_unslash_re.sub(
                _cookie_unslash_replace, cv[1:-1].encode()
            ).decode(errors="replace")

        out.append((ck, cv))

    return cls(out)

