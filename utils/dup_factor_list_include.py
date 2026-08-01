
def dup_factor_list_include(f, K):
    """Factor univariate polynomials into irreducibles in `K[x]`. """
    coeff, factors = dup_factor_list(f, K)

    if not factors:
        return [(dup_strip([coeff]), 1)]
    else:
        g = dup_mul_ground(factors[0][0], coeff, K)
        return [(g, factors[0][1])] + factors[1:]

