
def nth(n, seq):
    """ The nth element in a sequence

    >>> nth(1, 'ABC')
    'B'
    """
    if isinstance(seq, (tuple, list, Sequence)):
        return seq[n]
    else:
        return next(itertools.islice(seq, n, None))


def nth(iterable, n, default=None):
    """Returns the nth item or a default value.

    >>> l = range(10)
    >>> nth(l, 3)
    3
    >>> nth(l, 20, "zebra")
    'zebra'

    """
    return next(islice(iterable, n, None), default)

