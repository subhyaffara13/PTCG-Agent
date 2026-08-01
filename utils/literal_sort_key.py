
def literal_sort_key(value: object) -> tuple[object, ...]:
    """Return a sort key for a literal value."""
    if isinstance(value, frozenset):
        # Sort items to avoid depending on the unpredictable iteration order.
        return ("frozenset", tuple(sorted(literal_sort_key(item) for item in value)))
    elif isinstance(value, tuple):
        return ("tuple", tuple(literal_sort_key(item) for item in value))
    return (type(value).__name__, repr(value))

