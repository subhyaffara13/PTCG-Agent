
def dup_qq_i_factor(f, K0):
    """Factor univariate polynomials into irreducibles in `QQ_I[x]`. """
    # Factor in QQ<I>
    K1 = K0.as_AlgebraicField()
    f = dup_convert(f, K0, K1)
    coeff, factors = dup_factor_list(f, K1)
    factors = [(dup_convert(fac, K1, K0), i) for fac, i in factors]
    coeff = K0.convert(coeff, K1)
    return coeff, factors

