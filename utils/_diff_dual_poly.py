
def _diff_dual_poly(j, k, y, d, t):
    """
    d-th derivative of the dual polynomial $p_{j,k}(y)$
    """
    if d == 0:
        return _dual_poly(j, k, t, y)
    if d == k:
        return poch(1, k)
    comb = list(combinations(range(j + 1, j + k + 1), d))
    res = 0
    for i in range(len(comb) * len(comb[0])):
        res += np.prod([(y - t[j + p]) for p in range(1, k + 1)
                        if (j + p) not in comb[i//d]])
    return res

