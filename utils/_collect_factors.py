
def _collect_factors(factors_list):
    """
    Collect repeating factors and sort.

    >>> from sympy.polys.matrices.domainmatrix import _collect_factors
    >>> _collect_factors([([1, 2], 2), ([1, 4], 3), ([1, 2], 5)])
    [([1, 4], 3), ([1, 2], 7)]
    """
    factors = Counter()
    for factor, exponent in factors_list:
        factors[tuple(factor)] += exponent

    factors_list = [(list(f), e) for f, e in factors.items()]

    return _sort_factors(factors_list)

