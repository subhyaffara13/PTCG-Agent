
def powerset_of_sets(iterable):
    """Yields all possible subsets of the iterable.

        >>> list(powerset_of_sets([1, 2, 3]))  # doctest: +SKIP
        [set(), {1}, {2}, {3}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}]
        >>> list(powerset_of_sets([1, 1, 0]))  # doctest: +SKIP
        [set(), {1}, {0}, {0, 1}]

    :func:`powerset_of_sets` takes care to minimize the number
    of hash operations performed.
    """
    sets = tuple(dict.fromkeys(map(frozenset, zip(iterable))))
    return chain.from_iterable(
        starmap(set().union, combinations(sets, r))
        for r in range(len(sets) + 1)
    )

