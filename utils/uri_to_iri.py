
def uri_to_iri(uri: str) -> str:
    """Convert a URI to an IRI. All valid UTF-8 characters are unquoted,
    leaving all reserved and invalid characters quoted. If the URL has
    a domain, it is decoded from Punycode.

    >>> uri_to_iri("http://xn--n3h.net/p%C3%A5th?q=%C3%A8ry%DF")
    'http://\\u2603.net/p\\xe5th?q=\\xe8ry%DF'

    :param uri: The URI to convert.

    .. versionchanged:: 3.0
        Passing a tuple or bytes, and the ``charset`` and ``errors`` parameters,
        are removed.

    .. versionchanged:: 2.3
        Which characters remain quoted is specific to each part of the URL.

    .. versionchanged:: 0.15
        All reserved and invalid characters remain quoted. Previously,
        only some reserved characters were preserved, and invalid bytes
        were replaced instead of left quoted.

    .. versionadded:: 0.6
    """
    parts = urlsplit(uri)
    path = _unquote_path(parts.path)
    query = _unquote_query(parts.query)
    fragment = _unquote_fragment(parts.fragment)

    if parts.hostname:
        netloc = _decode_idna(parts.hostname)
    else:
        netloc = ""

    if ":" in netloc:
        netloc = f"[{netloc}]"

    if parts.port:
        netloc = f"{netloc}:{parts.port}"

    if parts.username:
        auth = _unquote_user(parts.username)

        if parts.password:
            password = _unquote_user(parts.password)
            auth = f"{auth}:{password}"

        netloc = f"{auth}@{netloc}"

    return urlunsplit((parts.scheme, netloc, path, query, fragment))

