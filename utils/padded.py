
def padded(iterable, fillvalue=None, n=None, next_multiple=False):
    """Yield the elements from *iterable*, followed by *fillvalue*, such that
    at least *n* items are emitted.

        >>> list(padded([1, 2, 3], '?', 5))
        [1, 2, 3, '?', '?']

    If *next_multiple* is ``True``, *fillvalue* will be emitted until the
    number of items emitted is a multiple of *n*:

        >>> list(padded([1, 2, 3, 4], n=3, next_multiple=True))
        [1, 2, 3, 4, None, None]

    If *n* is ``None``, *fillvalue* will be emitted indefinitely.

    To create an *iterable* of exactly size *n*, you can truncate with
    :func:`islice`.

        >>> list(islice(padded([1, 2, 3], '?'), 5))
        [1, 2, 3, '?', '?']
        >>> list(islice(padded([1, 2, 3, 4, 5, 6, 7, 8], '?'), 5))
        [1, 2, 3, 4, 5]

    """
    iterator = iter(iterable)
    iterator_with_repeat = chain(iterator, repeat(fillvalue))

    if n is None:
        return iterator_with_repeat
    elif n < 1:
        raise ValueError('n must be at least 1')
    elif next_multiple:

        def slice_generator():
            for first in iterator:
                yield (first,)
                yield islice(iterator_with_repeat, n - 1)

        # While elements exist produce slices of size n
        return chain.from_iterable(slice_generator())
    else:
        # Ensure the first batch is at least size n then iterate
        return chain(islice(iterator_with_repeat, n), iterator)

