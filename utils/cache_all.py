
def cache_all(value=True):
    """Sets whether to cache all patterns, even those are compiled explicitly.
    Passing None has no effect, but returns the current setting."""
    global _cache_all

    if value is None:
        return _cache_all

    _cache_all = value

