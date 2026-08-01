
def take_nth(n, seq):
    """ Every nth item in seq

    >>> list(take_nth(2, [10, 20, 30, 40, 50]))
    [10, 30, 50]
    """
    return itertools.islice(seq, 0, None, n)

