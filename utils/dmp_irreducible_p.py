
def dmp_irreducible_p(f, u, K):
    """
    Returns ``True`` if a multivariate polynomial ``f`` has no factors
    over its domain.
    """
    _, factors = dmp_factor_list(f, u, K)

    if not factors:
        return True
    elif len(factors) > 1:
        return False
    else:
        _, k = factors[0]
        return k == 1

