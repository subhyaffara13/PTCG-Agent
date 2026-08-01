
def outer_product(func, xs, ys, *args, **kwargs):
    """A generalized outer product that applies a binary function to all
    pairs of items. Returns a 2D matrix with ``len(xs)`` rows and ``len(ys)``
    columns.
    Also accepts ``*args`` and ``**kwargs`` that are passed to ``func``.

    Multiplication table:

    >>> list(outer_product(mul, range(1, 4), range(1, 6)))
    [(1, 2, 3, 4, 5), (2, 4, 6, 8, 10), (3, 6, 9, 12, 15)]

    Cross tabulation:

    >>> xs = ['A', 'B', 'A', 'A', 'B', 'B', 'A', 'A', 'B', 'B']
    >>> ys = ['X', 'X', 'X', 'Y', 'Z', 'Z', 'Y', 'Y', 'Z', 'Z']
    >>> pair_counts = Counter(zip(xs, ys))
    >>> count_rows = lambda x, y: pair_counts[x, y]
    >>> list(outer_product(count_rows, sorted(set(xs)), sorted(set(ys))))
    [(2, 3, 0), (1, 0, 4)]

    Usage with ``*args`` and ``**kwargs``:

    >>> animals = ['cat', 'wolf', 'mouse']
    >>> list(outer_product(min, animals, animals, key=len))
    [('cat', 'cat', 'cat'), ('cat', 'wolf', 'wolf'), ('cat', 'wolf', 'mouse')]
    """
    ys = tuple(ys)
    return batched(
        starmap(lambda x, y: func(x, y, *args, **kwargs), product(xs, ys)),
        n=len(ys),
    )

