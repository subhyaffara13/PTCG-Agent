
def _cache_normalize_path(path: str) -> str:
    """Normalize path with caching."""
    # _module_file calls abspath on every path in sys.path every time it's
    # called; on a larger codebase this easily adds up to half a second just
    # assembling path components. This cache alleviates that.
    if not path:  # don't cache result for ''
        return _normalize_path(path)
    return _cache_normalize_path_(path)

