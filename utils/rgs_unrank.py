
def RGS_unrank(rank, m):
    """
    Gives the unranked restricted growth string for a given
    superset size.

    Examples
    ========

    >>> from sympy.combinatorics.partitions import RGS_unrank
    >>> RGS_unrank(14, 4)
    [0, 1, 2, 3]
    >>> RGS_unrank(0, 4)
    [0, 0, 0, 0]
    """
    if m < 1:
        raise ValueError("The superset size must be >= 1")
    if rank < 0 or RGS_enum(m) <= rank:
        raise ValueError("Invalid arguments")

    L = [1] * (m + 1)
    j = 1
    D = RGS_generalized(m)
    for i in range(2, m + 1):
        v = D[m - i, j]
        cr = j*v
        if cr <= rank:
            L[i] = j + 1
            rank -= cr
            j += 1
        else:
            L[i] = int(rank / v + 1)
            rank %= v
    return [x - 1 for x in L[1:]]

