
def shuffled(values: Iterable[_T]) -> list[_T]:
    """Return the shuffled values.

    The shuffling is performed out-of-place (i.e., not done in-place).

    >>> cards = shuffled(Card.parse('AcAdAhAs'))
    >>> cards  # doctest: +ELLIPSIS
    [A..., A..., A..., A...]

    :param values: The values to shuffle.
    :return: The shuffled values.
    """
    values = list(values)

    shuffle(values)

    return values

