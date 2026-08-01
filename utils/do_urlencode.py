
def do_urlencode(
    value: t.Union[str, t.Mapping[str, t.Any], t.Iterable[t.Tuple[str, t.Any]]],
) -> str:
    """Quote data for use in a URL path or query using UTF-8.

    Basic wrapper around :func:`urllib.parse.quote` when given a
    string, or :func:`urllib.parse.urlencode` for a dict or iterable.

    :param value: Data to quote. A string will be quoted directly. A
        dict or iterable of ``(key, value)`` pairs will be joined as a
        query string.

    When given a string, "/" is not quoted. HTTP servers treat "/" and
    "%2F" equivalently in paths. If you need quoted slashes, use the
    ``|replace("/", "%2F")`` filter.

    .. versionadded:: 2.7
    """
    if isinstance(value, str) or not isinstance(value, abc.Iterable):
        return url_quote(value)

    if isinstance(value, dict):
        items: t.Iterable[t.Tuple[str, t.Any]] = value.items()
    else:
        items = value  # type: ignore

    return "&".join(
        f"{url_quote(k, for_qs=True)}={url_quote(v, for_qs=True)}" for k, v in items
    )

