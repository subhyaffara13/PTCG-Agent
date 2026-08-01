
def _check_iter(value: cabc.Iterable[V]) -> cabc.Iterator[V]:
    """Check if the value is iterable but not a string. Raises a type
    error, or return an iterator over the value.
    """
    if isinstance(value, str):
        raise TypeError

    return iter(value)

