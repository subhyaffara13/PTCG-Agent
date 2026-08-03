import itertools

def make_partition(items, test, check=True):
    """
    Partitions items into sets based on the outcome of ``test(item1, item2)``.
    Pairs of items for which `test` returns `True` end up in the same set.

    Parameters
    ----------
    items : collections.abc.Iterable[collections.abc.Hashable]
        Items to partition
    test : collections.abc.Callable[collections.abc.Hashable, collections.abc.Hashable]
        A function that will be called with 2 arguments, taken from items.
        Should return `True` if those 2 items match/tests so need to end up in the same
        part of the partition, and `False` otherwise.
    check : bool optional (default: True)
        If ``True``, check that the resulting partition satisfies the match criteria.
        Every item should match every item in its part and none outside the part.

    Returns
    -------
    list[set]
        A partition as a list of sets (the parts). Each set contains some of
        the items in `items`, such that all items are in exactly one part and every
        pair of items in each part matches. The following will be true:
        ``all(thing_matcher(*pair) for pair in itertools.combinations(items, 2))``

    Notes
    -----
    The function `test` is assumed to be transitive: if ``test(a, b)`` and
    ``test(b, c)`` return ``True``, then ``test(a, c)`` must also be ``True``.
    The function `test` is assumed to be commutative: if ``test(a, b)``
    returns ``True`` then ``test(b, a)`` returns ``True``.
    """
    partition = []
    for item in items:
        for part in partition:
            p_item = next(iter(part))
            if test(item, p_item):
                part.add(item)
                break
        else:  # No break
            partition.append({item})

    if check:
        if not all(
            test(t1, t2) and test(t2, t1)
            for part in partition
            for t1, t2 in itertools.combinations(part, 2)
        ):
            raise nx.NetworkXError(
                f"\nInvalid partition created with {test}.\n"
                "Some items in a part do not match. This leads to\n"
                f"{partition=}"
            )
        if not all(
            not test(t1, t2) and not test(t2, t1)
            for p1 in partition
            for p2 in partition
            if p1 != p2
            for t1, t2 in itertools.product(p1, p2)
        ):
            raise nx.NetworkXError(
                f"\nInvalid partition created with {test}.\n"
                "Some items match multiple parts. This leads to\n"
                f"{partition=}"
            )
    return [set(part) for part in partition]

