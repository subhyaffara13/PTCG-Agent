
def _first(it: Iterable[_T]) -> _T | None:
    """Return the first value from any iterable.

    Returns ``None`` if the iterable is empty.
    """
    for val in it:
        return val
    return None


def _first(d):
    return next(iter(d.values()))

