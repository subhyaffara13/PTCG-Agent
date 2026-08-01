
def grouper(iterable, n, incomplete='fill', fillvalue=None):
    """Group elements from *iterable* into fixed-length groups of length *n*.

    >>> list(grouper('ABCDEF', 3))
    [('A', 'B', 'C'), ('D', 'E', 'F')]

    The keyword arguments *incomplete* and *fillvalue* control what happens for
    iterables whose length is not a multiple of *n*.

    When *incomplete* is `'fill'`, the last group will contain instances of
    *fillvalue*.

    >>> list(grouper('ABCDEFG', 3, incomplete='fill', fillvalue='x'))
    [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'x', 'x')]

    When *incomplete* is `'ignore'`, the last group will not be emitted.

    >>> list(grouper('ABCDEFG', 3, incomplete='ignore', fillvalue='x'))
    [('A', 'B', 'C'), ('D', 'E', 'F')]

    When *incomplete* is `'strict'`, a subclass of `ValueError` will be raised.

    >>> iterator = grouper('ABCDEFG', 3, incomplete='strict')
    >>> list(iterator)  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    UnequalIterablesError

    """
    iterators = [iter(iterable)] * n
    if incomplete == 'fill':
        return zip_longest(*iterators, fillvalue=fillvalue)
    if incomplete == 'strict':
        return _zip_equal(*iterators)
    if incomplete == 'ignore':
        return zip(*iterators)
    else:
        raise ValueError('Expected fill, strict, or ignore')

