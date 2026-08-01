
def partial_product(*iterables):
    """Yields tuples containing one item from each iterator, with subsequent
    tuples changing a single item at a time by advancing each iterator until it
    is exhausted. This sequence guarantees every value in each iterable is
    output at least once without generating all possible combinations.

    This may be useful, for example, when testing an expensive function.

        >>> list(partial_product('AB', 'C', 'DEF'))
        [('A', 'C', 'D'), ('B', 'C', 'D'), ('B', 'C', 'E'), ('B', 'C', 'F')]
    """

    iterators = list(map(iter, iterables))

    try:
        prod = [next(it) for it in iterators]
    except StopIteration:
        return
    yield tuple(prod)

    for i, it in enumerate(iterators):
        for prod[i] in it:
            yield tuple(prod)

