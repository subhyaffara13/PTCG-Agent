import itertools

def sliding_window(n, seq):
    """ A sequence of overlapping subsequences

    >>> list(sliding_window(2, [1, 2, 3, 4]))
    [(1, 2), (2, 3), (3, 4)]

    This function creates a sliding window suitable for transformations like
    sliding means / smoothing

    >>> mean = lambda seq: float(sum(seq)) / len(seq)
    >>> list(map(mean, sliding_window(2, [1, 2, 3, 4])))
    [1.5, 2.5, 3.5]
    """
    return zip(*(collections.deque(itertools.islice(it, i), 0) or it
               for i, it in enumerate(itertools.tee(seq, n))))


def sliding_window(iterable, n):
    """Return a sliding window of width *n* over *iterable*.

        >>> list(sliding_window(range(6), 4))
        [(0, 1, 2, 3), (1, 2, 3, 4), (2, 3, 4, 5)]

    If *iterable* has fewer than *n* items, then nothing is yielded:

        >>> list(sliding_window(range(3), 4))
        []

    For a variant with more features, see :func:`windowed`.
    """
    if n > 20:
        return _sliding_window_deque(iterable, n)
    elif n > 2:
        return _sliding_window_islice(iterable, n)
    elif n == 2:
        return pairwise(iterable)
    elif n == 1:
        return zip(iterable)
    else:
        raise ValueError(f'n should be at least one, not {n}')

