
def stable_literal_repr(obj: object) -> str:
    """Return a single-line repr of a literal value.

    Behaves like repr() for most values, but renders frozenset members in a
    deterministic order (frozenset iteration order is hash-seed dependent).
    """
    if isinstance(obj, frozenset):
        if not obj:
            return "frozenset()"
        items = ", ".join(stable_literal_repr(item) for item in sorted(obj, key=literal_sort_key))
        return "frozenset({" + items + "})"
    elif isinstance(obj, tuple):
        if len(obj) == 1:
            return "(" + stable_literal_repr(obj[0]) + ",)"
        return "(" + ", ".join(stable_literal_repr(item) for item in obj) + ")"
    return repr(obj)

