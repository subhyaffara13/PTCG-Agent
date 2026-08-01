
def _find_arbitrary_callable(
    args: tuple[object, ...], kwargs: dict[str, object]
) -> object:
    """
    Recursively searches args and kwargs for any arbitrary callable.
    Returns the first arbitrary callable found, or None if none exist.
    """
    found = None

    _T = TypeVar("_T")

    def check(obj: _T) -> _T:
        nonlocal found
        if found is not None:
            return obj
        if _is_arbitrary_callable(obj):
            found = obj
        return obj

    tree_map_(check, args)
    tree_map_(check, kwargs)
    return found

