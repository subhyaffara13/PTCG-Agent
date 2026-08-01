
def RGS_rank(rgs):
    """
    Computes the rank of a restricted growth string.

    Examples
    ========

    >>> from sympy.combinatorics.partitions import RGS_rank, RGS_unrank
    >>> RGS_rank([0, 1, 2, 1, 3])
    42
    >>> RGS_rank(RGS_unrank(4, 7))
    4
    """
    rgs_size = len(rgs)
    rank = 0
    D = RGS_generalized(rgs_size)
    for i in range(1, rgs_size):
        n = len(rgs[(i + 1):])
        m = max(rgs[0:i])
        rank += D[n, m + 1] * rgs[i]
    return rank

