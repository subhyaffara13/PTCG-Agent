
def last(seq):
    """ The last element in a sequence

    >>> last('ABC')
    'C'
    """
    return tail(1, seq)[0]


def last(iterable, default=_marker):
    """Return the last item of *iterable*, or *default* if *iterable* is
    empty.

        >>> last([0, 1, 2, 3])
        3
        >>> last([], 'some default')
        'some default'

    If *default* is not provided and there are no items in the iterable,
    raise ``ValueError``.
    """
    try:
        if isinstance(iterable, Sequence):
            return iterable[-1]
        # Work around https://bugs.python.org/issue38525
        if getattr(iterable, '__reversed__', None):
            return next(reversed(iterable))
        return deque(iterable, maxlen=1)[-1]
    except (IndexError, TypeError, StopIteration):
        if default is _marker:
            raise ValueError(
                'last() was called on an empty iterable, '
                'and no default value was provided.'
            )
        return default

