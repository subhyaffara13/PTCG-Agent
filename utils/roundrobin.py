
def roundrobin(*iterables):
    """roundrobin recipe taken from itertools documentation:
    https://docs.python.org/3/library/itertools.html#itertools-recipes

    roundrobin('ABC', 'D', 'EF') --> A D E B F C

    Recipe credited to George Sakkis
    """
    nexts = cycle(iter(it).__next__ for it in iterables)

    pending = len(iterables)
    while pending:
        try:
            for nxt in nexts:
                yield nxt()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))


def roundrobin(*iterables):
    """Visit input iterables in a cycle until each is exhausted.

        >>> list(roundrobin('ABC', 'D', 'EF'))
        ['A', 'D', 'E', 'B', 'F', 'C']

    This function produces the same output as :func:`interleave_longest`, but
    may perform better for some inputs (in particular when the number of
    iterables is small).

    """
    # Algorithm credited to George Sakkis
    iterators = map(iter, iterables)
    for num_active in range(len(iterables), 0, -1):
        iterators = cycle(islice(iterators, num_active))
        yield from map(next, iterators)

