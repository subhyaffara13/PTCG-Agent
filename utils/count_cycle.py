
def count_cycle(iterable, n=None):
    """Cycle through the items from *iterable* up to *n* times, yielding
    the number of completed cycles along with each item. If *n* is omitted the
    process repeats indefinitely.

    >>> list(count_cycle('AB', 3))
    [(0, 'A'), (0, 'B'), (1, 'A'), (1, 'B'), (2, 'A'), (2, 'B')]

    """
    seq = tuple(iterable)
    if not seq:
        return iter(())
    counter = count() if n is None else range(n)
    return zip(repeat_each(counter, len(seq)), cycle(seq))

