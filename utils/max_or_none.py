from typing import Any

def max_or_none(values: Iterable[Any], key: Any = None) -> Any:
    """Get the maximum value while ignoring ``None`` values.

    If the iterable of values are empty, ``None`` is returned.

    >>> max_or_none([1, 2, 3, -2, -1])
    3
    >>> max_or_none([1, None, 2, None, 3, -2, -1, None])
    3
    >>> max_or_none([]) is None
    True

    :param values: The optional values.
    :param key: The optional key function.
    :return: The maximum value. If the values are empty, ``None``.
    """
    try:
        return max(filter_none(values), key=key)
    except ValueError:
        return None

