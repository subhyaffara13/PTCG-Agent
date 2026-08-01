
def rotated(values: Iterable[_T], count: int) -> deque[_T]:
    """Rotate the values.

    The rotation is performed out-of-place (i.e., not done in-place).

    >>> rotated(['a', 'b', 'c', 'd'], 2)
    deque(['c', 'd', 'a', 'b'])
    >>> rotated(range(5), -3)
    deque([3, 4, 0, 1, 2])

    :param values: The values to rotate.
    :param count: The rotation.
    :return: The rotated values.
    """
    values = deque(values)

    values.rotate(count)

    return values

