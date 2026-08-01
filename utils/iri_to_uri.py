
def iri_to_uri(iri: str) -> str:
    """Convert an IRI to a URI. All non-ASCII and unsafe characters are
    quoted. If the URL has a domain, it is encoded to Punycode.

    >>> iri_to_uri('http://\\u2603.net/p\\xe5th?q=\\xe8ry%DF')
    'http://xn--n3h.net/p%C3%A5th?q=%C3%A8ry%DF'

    :param iri: The IRI to convert.

    .. versionchanged:: 3.0
        Passing a tuple or bytes, the ``charset`` and ``errors`` parameters,
        and the ``safe_conversion`` parameter, are removed.

    .. versionchanged:: 2.3
        Which characters remain unquoted is specific to each part of the URL.

    .. versionchanged:: 0.15
        All reserved characters remain unquoted. Previously, only some reserved
        characters were left unquoted.

    .. versionchanged:: 0.9.6
       The ``safe_conversion`` parameter was added.

    .. versionadded:: 0.6
    """
    parts = urlsplit(iri)
    # safe = https://url.spec.whatwg.org/#url-path-segment-string
    # as well as percent for things that are already quoted
    path = quote(parts.path, safe="%!$&'()*+,/:;=@")
    query = quote(parts.query, safe="%!$&'()*+,/:;=?@")
    fragment = quote(parts.fragment, safe="%!#$&'()*+,/:;=?@")

    if parts.hostname:
        netloc = parts.hostname.encode("idna").decode("ascii")
    else:
        netloc = ""

    if ":" in netloc:
        netloc = f"[{netloc}]"

    if parts.port:
        netloc = f"{netloc}:{parts.port}"

    if parts.username:
        auth = quote(parts.username, safe="%!$&'()*+,;=")

        if parts.password:
            password = quote(parts.password, safe="%!$&'()*+,;=")
            auth = f"{auth}:{password}"

        netloc = f"{auth}@{netloc}"

    return urlunsplit((parts.scheme, netloc, path, query, fragment))

