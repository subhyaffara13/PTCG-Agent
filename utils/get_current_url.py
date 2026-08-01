
def get_current_url(
    environ: WSGIEnvironment,
    root_only: bool = False,
    strip_querystring: bool = False,
    host_only: bool = False,
    trusted_hosts: t.Collection[str] | None = None,
) -> str:
    """Recreate the URL for a request from the parts in a WSGI
    environment.

    The URL is an IRI, not a URI, so it may contain Unicode characters.
    Use :func:`~werkzeug.urls.iri_to_uri` to convert it to ASCII.

    :param environ: The WSGI environment to get the URL parts from.
    :param root_only: Only build the root path, don't include the
        remaining path or query string.
    :param strip_querystring: Don't include the query string.
    :param host_only: Only build the scheme and host.
    :param trusted_hosts: A list of trusted host names to validate the
        host against.
    """
    parts = {
        "scheme": environ["wsgi.url_scheme"],
        "host": get_host(environ, trusted_hosts),
    }

    if not host_only:
        parts["root_path"] = environ.get("SCRIPT_NAME", "")

        if not root_only:
            parts["path"] = environ.get("PATH_INFO", "")

            if not strip_querystring:
                parts["query_string"] = environ.get("QUERY_STRING", "").encode("latin1")

    return _sansio_utils.get_current_url(**parts)


def get_current_url(
    scheme: str,
    host: str,
    root_path: str | None = None,
    path: str | None = None,
    query_string: bytes | None = None,
) -> str:
    """Recreate the URL for a request. If an optional part isn't
    provided, it and subsequent parts are not included in the URL.

    The URL is an IRI, not a URI, so it may contain Unicode characters.
    Use :func:`~werkzeug.urls.iri_to_uri` to convert it to ASCII.

    :param scheme: The protocol the request used, like ``"https"``.
    :param host: The host the request was made to. See :func:`get_host`.
    :param root_path: Prefix that the application is mounted under. This
        is prepended to ``path``.
    :param path: The path part of the URL after ``root_path``.
    :param query_string: The portion of the URL after the "?".
    """
    url = [scheme, "://", host]

    if root_path is None:
        url.append("/")
        return uri_to_iri("".join(url))

    # safe = https://url.spec.whatwg.org/#url-path-segment-string
    # as well as percent for things that are already quoted
    url.append(quote(root_path.rstrip("/"), safe="!$&'()*+,/:;=@%"))
    url.append("/")

    if path is None:
        return uri_to_iri("".join(url))

    url.append(quote(path.lstrip("/"), safe="!$&'()*+,/:;=@%"))

    if query_string:
        url.append("?")
        url.append(quote(query_string, safe="!$&'()*+,/:;=?@%"))

    return uri_to_iri("".join(url))

