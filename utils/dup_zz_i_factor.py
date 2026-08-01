
def dup_zz_i_factor(f, K0):
    """Factor univariate polynomials into irreducibles in `ZZ_I[x]`. """
    # First factor in QQ_I
    K1 = K0.get_field()
    f = dup_convert(f, K0, K1)
    coeff, factors = dup_qq_i_factor(f, K1)

    new_factors = []
    for fac, i in factors:
        # Extract content
        fac_denom, fac_num = dup_clear_denoms(fac, K1)
        fac_num_ZZ_I = dup_convert(fac_num, K1, K0)
        content, fac_prim = dmp_ground_primitive(fac_num_ZZ_I, 0, K0)

        coeff = (coeff * content ** i) // fac_denom ** i
        new_factors.append((fac_prim, i))

    factors = new_factors
    coeff = K0.convert(coeff, K1)
    return coeff, factors

