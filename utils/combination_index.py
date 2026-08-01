
def combination_index(element, iterable):
    """Equivalent to ``list(combinations(iterable, r)).index(element)``

    The subsequences of *iterable* that are of length *r* can be ordered
    lexicographically. :func:`combination_index` computes the index of the
    first *element*, without computing the previous combinations.

        >>> combination_index('adf', 'abcdefg')
        10

    ``ValueError`` will be raised if the given *element* isn't one of the
    combinations of *iterable*.
    """
    element = enumerate(element)
    k, y = next(element, (None, None))
    if k is None:
        return 0

    indexes = []
    pool = enumerate(iterable)
    for n, x in pool:
        if x == y:
            indexes.append(n)
            tmp, y = next(element, (None, None))
            if tmp is None:
                break
            else:
                k = tmp
    else:
        raise ValueError('element is not a combination of iterable')

    n, _ = last(pool, default=(n, None))

    # Python versions below 3.8 don't have math.comb
    index = 1
    for i, j in enumerate(reversed(indexes), start=1):
        j = n - j
        if i <= j:
            index += comb(j, i)

    return comb(n + 1, k + 1) - index

