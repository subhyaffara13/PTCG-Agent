
def _dmp_sqf_norm_shifts(f, u, K):
    """Generate a sequence of candidate shifts for dmp_sqf_norm."""
    #
    # We want to find a minimal shift if possible because shifting high degree
    # variables can be expensive e.g. x**10 -> (x + 1)**10. We try a few easy
    # cases first before the final infinite loop that is guaranteed to give
    # only finitely many bad shifts (see Trager76 for proof of this in the
    # univariate case).
    #

    # First the trivial shift [0, 0, ...]
    n = u + 1
    s0 = [0] * n
    yield s0, f

    # Shift in multiples of the generator of the extension field K
    a = K.unit

    # Variables of degree > 0 ordered by increasing degree
    d = dmp_degree_list(f, u)
    var_indices = [i for di, i in sorted(zip(d, range(u+1))) if di > 0]

    # Now try [1, 0, 0, ...], [0, 1, 0, ...]
    for i in var_indices:
        s1 = s0.copy()
        s1[i] = 1
        a1 = [-a*s1i for s1i in s1]
        f1 = dmp_shift(f, a1, u, K)
        yield s1, f1

    # Now try [1, 1, 1, ...], [2, 2, 2, ...]
    j = 0
    while True:
        j += 1
        sj = [j] * n
        aj = [-a*j] * n
        fj = dmp_shift(f, aj, u, K)
        yield sj, fj

