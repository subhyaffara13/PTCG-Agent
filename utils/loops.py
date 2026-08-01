
def loops(n):
    """Returns an iterable with *n* elements for efficient looping.
    Like ``range(n)`` but doesn't create integers.

    >>> i = 0
    >>> for _ in loops(5):
    ...     i += 1
    >>> i
    5

    """
    return repeat(None, n)

