
def _dup_check_degrees(f, result):
    """Sanity check the degrees of a computed factorization in K[x]."""
    deg = sum(k * dup_degree(fac) for (fac, k) in result)
    assert deg == dup_degree(f)

