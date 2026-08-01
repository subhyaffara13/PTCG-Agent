
def pre_encoded_url(url_str: str) -> "URL":
    """Parse pre-encoded URL."""
    self = object.__new__(URL)
    val = split_url(url_str)
    self._scheme, self._netloc, self._path, self._query, self._fragment = val
    self._cache = {}
    return self

