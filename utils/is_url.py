
def is_url(name: str) -> bool:
    """
    Return true if the name looks like a URL.

    For example:
    >>> is_url("name@http://foo.com")
    False
    >>> is_url("git+http://foo.com")
    True
    >>> is_url("ftp://foo.com")
    True
    >>> is_url("file://foo.com")
    True
    >>> is_url("git://foo.com")
    False
    >>> is_url("www.foo.com")
    False
    """
    scheme = get_url_scheme(name)
    if scheme is None:
        return False
    return scheme in ["http", "https", "file", "ftp"] + vcs_all_schemes


def is_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_url(string):
    """Checks if the passed string contains a valid url and nothing else. e.g. if space is included it's immediately
    invalidated the url"""
    if " " in string:
        return False
    result = urlparse(string)
    return all([result.scheme, result.netloc])


def is_url(val) -> bool:
    return isinstance(val, str) and val.startswith("http")


def is_url(val) -> bool:
    return isinstance(val, str) and val.startswith("http")


def is_url(val) -> bool:
    return isinstance(val, str) and val.startswith("http")


def is_url(name: str) -> bool:
    """
    Return true if the name looks like a URL.
    """
    scheme = urllib.parse.urlsplit(name).scheme
    if not scheme:
        return False
    return scheme in ["http", "https", "file", "ftp"] + vcs.all_schemes


def is_url(url: object) -> bool:
    """
    Check to see if a URL has a valid protocol.

    Parameters
    ----------
    url : str or unicode

    Returns
    -------
    isurl : bool
        If `url` has a valid protocol return True otherwise False.
    """
    if not isinstance(url, str):
        return False
    return parse_url(url).scheme in _VALID_URLS

