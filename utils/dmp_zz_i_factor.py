
def dmp_zz_i_factor(f, u, K0):
    """Factor multivariate polynomials into irreducibles in `ZZ_I[X]`. """
    # First factor in QQ_I
    K1 = K0.get_field()
    f = dmp_convert(f, u, K0, K1)
    coeff, factors = dmp_qq_i_factor(f, u, K1)

    new_factors = []
    for fac, i in factors:
        # Extract content
        fac_denom, fac_num = dmp_clear_denoms(fac, u, K1)
        fac_num_ZZ_I = dmp_convert(fac_num, u, K1, K0)
        content, fac_prim = dmp_ground_primitive(fac_num_ZZ_I, u, K0)

        coeff = (coeff * content ** i) // fac_denom ** i
        new_factors.append((fac_prim, i))

    factors = new_factors
    coeff = K0.convert(coeff, K1)
    return coeff, factors

