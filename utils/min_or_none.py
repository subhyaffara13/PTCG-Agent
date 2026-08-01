
def min_or_none(values: Iterable[Any], key: Any = None) -> Any:
    """Get the minimum value while ignoring ``None`` values.

    If the iterable of values are empty, ``None`` is returned.

    >>> min_or_none([1, 2, 3, -2, -1])
    -2
    >>> min_or_none([1, None, 2, None, 3, -2, -1, None])
    -2
    >>> min_or_none([]) is None
    True

    :param values: The optional values.
    :param key: The optional key function.
    :return: The minimum value. If the values are empty, ``None``.
    """
    try:
        return min(filter_none(values), key=key)
    except ValueError:
        return None

