
def duplicates_justseen(iterable, key=None):
    """Yields serially-duplicate elements after their first appearance.

    >>> list(duplicates_justseen('mississippi'))
    ['s', 's', 'p']
    >>> list(duplicates_justseen('AaaBbbCccAaa', str.lower))
    ['a', 'a', 'b', 'b', 'c', 'c', 'a', 'a']

    This function is analogous to :func:`unique_justseen`.

    """
    return flatten(g for _, g in groupby(iterable, key) for _ in g)

