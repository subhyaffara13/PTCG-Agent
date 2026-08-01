
def clean_values(values: ValuesLike, count: int) -> tuple[int, ...]:
    """Clean the numerical values.

    This function "cleans" any values-like object (e.g., iterables,
    mappings, an number, etc.) into a tuple of numerical values.

    >>> clean_values([1, 2, 3, 4], 4)
    (1, 2, 3, 4)
    >>> clean_values([1, 2, 3, 4], 6)
    (1, 2, 3, 4, 0, 0)
    >>> clean_values({0: 1, -1: 2}, 4)
    (1, 0, 0, 2)
    >>> clean_values(4, 4)
    (4, 4, 4, 4)
    >>> clean_values((1, 2, 3), 2)
    (1, 2)
    >>> clean_values(None, 2)
    Traceback (most recent call last):
        ...
    ValueError: The values None are invalid.

    :param values: The values.
    :param count: The number of values.
    :return: The cleaned numerical values.
    :raises ValueError: If the values are invalid.
    """
    if isinstance(values, Number):
        values = cast(tuple[int, ...], (values,) * count)
    elif isinstance(values, Mapping):
        parsed_values = [0] * count

        for key, value in values.items():
            parsed_values[key] += value

        values = tuple(parsed_values)
    elif isinstance(values, Iterable):
        parsed_values = list(values)[:count]

        while len(parsed_values) < count:
            parsed_values.append(0)

        values = tuple(parsed_values)
    else:
        raise ValueError(f'The values {repr(values)} are invalid.')

    return values

