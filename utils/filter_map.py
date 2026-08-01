
def filter_map(func, iterable):
    """Apply *func* to every element of *iterable*, yielding only those which
    are not ``None``.

    >>> elems = ['1', 'a', '2', 'b', '3']
    >>> list(filter_map(lambda s: int(s) if s.isnumeric() else None, elems))
    [1, 2, 3]
    """
    for x in iterable:
        y = func(x)
        if y is not None:
            yield y

