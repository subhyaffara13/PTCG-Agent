
def takewhile_inclusive(predicate, iterable):
    """A variant of :func:`takewhile` that yields one additional element.

        >>> list(takewhile_inclusive(lambda x: x < 5, [1, 4, 6, 4, 1]))
        [1, 4, 6]

    :func:`takewhile` would return ``[1, 4]``.
    """
    for x in iterable:
        yield x
        if not predicate(x):
            break

