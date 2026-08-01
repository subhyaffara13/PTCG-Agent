
def quantify(iterable, pred=bool):
    """Return the how many times the predicate is true.

    >>> quantify([True, False, True])
    2

    """
    return sum(map(pred, iterable))

