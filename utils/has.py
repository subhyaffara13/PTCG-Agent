
def has(cls):
    """
    Check whether *cls* is a class with *attrs* attributes.

    Args:
        cls (type): Class to introspect.

    Raises:
        TypeError: If *cls* is not a class.

    Returns:
        bool:
    """
    attrs = getattr(cls, "__attrs_attrs__", None)
    if attrs is not None:
        return True

    # No attrs, maybe it's a specialized generic (A[str])?
    generic_base = get_generic_base(cls)
    if generic_base is not None:
        generic_attrs = getattr(generic_base, "__attrs_attrs__", None)
        if generic_attrs is not None:
            # Stick it on here for speed next time.
            cls.__attrs_attrs__ = generic_attrs
        return generic_attrs is not None
    return False


def has(
    o: Any,
    classinfo: Type | None = None,
    default: Any = None,
    path: list[str] | None = None,
    is_callable: bool | None = None,
) -> bool:
    if path is None:
        path = []
    try:
        cur = o
        for p in path:
            cur = cur[p]
        if classinfo is not None and not isinstance(cur, classinfo):
            raise ValueError("Not a match")
        if is_callable and not callable(cur):
            raise ValueError("Not callable")
        if not is_callable and callable(cur):
            raise ValueError("Is callable")
        return True
    except Exception:
        if default is not None and o is not None and len(path) > 0:
            cur = o
            for p in path[:-1]:
                if not has(cur, dict, path=[p]):
                    cur[p] = {}
                cur = cur[p]
            cur[path[-1]] = default
        return False

