
def dmp_trial_division(f, factors, u, K):
    """
    Determine multiplicities of factors for a multivariate polynomial
    using trial division.

    An error will be raised if any factor does not divide ``f``.
    """
    result = []

    for factor in factors:
        k = 0

        while True:
            q, r = dmp_div(f, factor, u, K)

            if dmp_zero_p(r, u):
                f, k = q, k + 1
            else:
                break

        if k == 0:
            raise RuntimeError("trial division failed")

        result.append((factor, k))

    return _sort_factors(result)

