
def locate(iterable, pred=bool, window_size=None):
    """Yield the index of each item in *iterable* for which *pred* returns
    ``True``.

    *pred* defaults to :func:`bool`, which will select truthy items:

        >>> list(locate([0, 1, 1, 0, 1, 0, 0]))
        [1, 2, 4]

    Set *pred* to a custom function to, e.g., find the indexes for a particular
    item.

        >>> list(locate(['a', 'b', 'c', 'b'], lambda x: x == 'b'))
        [1, 3]

    If *window_size* is given, then the *pred* function will be called with
    that many items. This enables searching for sub-sequences:

        >>> iterable = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
        >>> pred = lambda *args: args == (1, 2, 3)
        >>> list(locate(iterable, pred=pred, window_size=3))
        [1, 5, 9]

    Use with :func:`seekable` to find indexes and then retrieve the associated
    items:

        >>> from itertools import count
        >>> from more_itertools import seekable
        >>> source = (3 * n + 1 if (n % 2) else n // 2 for n in count())
        >>> it = seekable(source)
        >>> pred = lambda x: x > 100
        >>> indexes = locate(it, pred=pred)
        >>> i = next(indexes)
        >>> it.seek(i)
        >>> next(it)
        106

    """
    if window_size is None:
        return compress(count(), map(pred, iterable))

    if window_size < 1:
        raise ValueError('window size must be at least 1')

    it = windowed(iterable, window_size, fillvalue=_marker)
    return compress(count(), starmap(pred, it))

