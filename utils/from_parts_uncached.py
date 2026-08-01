
def from_parts_uncached(
    scheme: str, netloc: str, path: str, query: str, fragment: str
) -> "URL":
    """Create a new URL from parts."""
    self = object.__new__(URL)
    self._scheme = scheme
    self._netloc = netloc
    self._path = path
    self._query = query
    self._fragment = fragment
    self._cache = {}
    return self

