
def _dmp_check_degrees(f, u, result):
    """Sanity check the degrees of a computed factorization in K[X]."""
    degs = [0] * (u + 1)
    for fac, k in result:
        degs_fac = dmp_degree_list(fac, u)
        degs = [d1 + k * d2 for d1, d2 in zip(degs, degs_fac)]
    assert tuple(degs) == dmp_degree_list(f, u)

