
def repeat_last(iterable, default=None):
    """After the *iterable* is exhausted, keep yielding its last element.

        >>> list(islice(repeat_last(range(3)), 5))
        [0, 1, 2, 2, 2]

    If the iterable is empty, yield *default* forever::

        >>> list(islice(repeat_last(range(0), 42), 5))
        [42, 42, 42, 42, 42]

    """
    item = _marker
    for item in iterable:
        yield item
    final = default if item is _marker else item
    yield from repeat(final)

