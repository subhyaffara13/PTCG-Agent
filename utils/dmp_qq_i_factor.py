
def dmp_qq_i_factor(f, u, K0):
    """Factor multivariate polynomials into irreducibles in `QQ_I[X]`. """
    # Factor in QQ<I>
    K1 = K0.as_AlgebraicField()
    f = dmp_convert(f, u, K0, K1)
    coeff, factors = dmp_factor_list(f, u, K1)
    factors = [(dmp_convert(fac, u, K1, K0), i) for fac, i in factors]
    coeff = K0.convert(coeff, K1)
    return coeff, factors

