
def _rec_diff_eval(g, m, a, v, i, j, K):
    """Recursive helper for :func:`dmp_diff_eval`."""
    if i == j:
        return dmp_eval(dmp_diff(g, m, v, K), a, v, K)

    v, i = v - 1, i + 1

    return dmp_strip([ _rec_diff_eval(c, m, a, v, i, j, K) for c in g ], v)

