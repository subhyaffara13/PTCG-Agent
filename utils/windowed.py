
def windowed(seq, n, fillvalue=None, step=1):
    """Return a sliding window of width *n* over the given iterable.

        >>> all_windows = windowed([1, 2, 3, 4, 5], 3)
        >>> list(all_windows)
        [(1, 2, 3), (2, 3, 4), (3, 4, 5)]

    When the window is larger than the iterable, *fillvalue* is used in place
    of missing values:

        >>> list(windowed([1, 2, 3], 4))
        [(1, 2, 3, None)]

    Each window will advance in increments of *step*:

        >>> list(windowed([1, 2, 3, 4, 5, 6], 3, fillvalue='!', step=2))
        [(1, 2, 3), (3, 4, 5), (5, 6, '!')]

    To slide into the iterable's items, use :func:`chain` to add filler items
    to the left:

        >>> iterable = [1, 2, 3, 4]
        >>> n = 3
        >>> padding = [None] * (n - 1)
        >>> list(windowed(chain(padding, iterable), 3))
        [(None, None, 1), (None, 1, 2), (1, 2, 3), (2, 3, 4)]
    """
    if n < 0:
        raise ValueError('n must be >= 0')
    if n == 0:
        yield ()
        return
    if step < 1:
        raise ValueError('step must be >= 1')

    iterator = iter(seq)

    # Generate first window
    window = deque(islice(iterator, n), maxlen=n)

    # Deal with the first window not being full
    if not window:
        return
    if len(window) < n:
        yield tuple(window) + ((fillvalue,) * (n - len(window)))
        return
    yield tuple(window)

    # Create the filler for the next windows. The padding ensures
    # we have just enough elements to fill the last window.
    padding = (fillvalue,) * (n - 1 if step >= n else step - 1)
    filler = map(window.append, chain(iterator, padding))

    # Generate the rest of the windows
    for _ in islice(filler, step - 1, None, step):
        yield tuple(window)

