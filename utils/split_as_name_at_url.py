
def split_as_name_at_url(reqstr: str) -> NamedTuple:
    """
    Split ``reqstr`` and return a NameAtUrl tuple or None if this is not
    a PEP-508-like requirement such as:
    foo @ https://fooo.com/bar.tgz

    For example::
    >>> assert split_as_name_at_url("foo") == None
    >>> assert split_as_name_at_url("") is None

    >>> split = split_as_name_at_url("foo@https://example.com")
    >>> expected = NameAtUrl(spec='foo', url='https://example.com')
    >>> assert split == expected, split

    >>> split = split_as_name_at_url("fo/o@https://example.com")
    >>> assert split is None

    >>> split = split_as_name_at_url("foo@example.com")
    >>> assert split is None

    >>> split = split_as_name_at_url("foo@git+https://example.com")
    >>> expected = NameAtUrl(spec='foo', url='git+https://example.com')
    >>> assert split == expected, split
    """
    if not reqstr:
        return
    if "@" in reqstr:
        # If the path contains '@' and the part before it does not look
        # like a path, try to treat it as a PEP 508 URL req.
        spec, _, url = reqstr.partition("@")
        spec = spec.strip()
        url = url.strip()
        if not _looks_like_path(spec) and is_url(url):
            return NameAtUrl(spec, url)

