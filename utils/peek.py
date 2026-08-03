import itertools

def peek(seq):
    """ Retrieve the next element of a sequence

    Returns the first element and an iterable equivalent to the original
    sequence, still having the element retrieved.

    >>> seq = [0, 1, 2, 3, 4]
    >>> first, seq = peek(seq)
    >>> first
    0
    >>> list(seq)
    [0, 1, 2, 3, 4]
    """
    iterator = iter(seq)
    item = next(iterator)
    return item, itertools.chain((item,), iterator)

