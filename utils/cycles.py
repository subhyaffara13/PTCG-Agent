
def cycles(seq):
    """Yields cyclic permutations of the given sequence.

    For example::

        >>> list(cycles("abc"))
        [('a', 'b', 'c'), ('b', 'c', 'a'), ('c', 'a', 'b')]

    """
    n = len(seq)
    cycled_seq = cycle(seq)
    for x in seq:
        yield tuple(islice(cycled_seq, n))
        next(cycled_seq)

