
def dup_factor_list(f, K0):
    """Factor univariate polynomials into irreducibles in `K[x]`. """
    j, f = dup_terms_gcd(f, K0)
    cont, f = dup_primitive(f, K0)

    if K0.is_FiniteField:
        coeff, factors = dup_gf_factor(f, K0)
    elif K0.is_Algebraic:
        coeff, factors = dup_ext_factor(f, K0)
    elif K0.is_GaussianRing:
        coeff, factors = dup_zz_i_factor(f, K0)
    elif K0.is_GaussianField:
        coeff, factors = dup_qq_i_factor(f, K0)
    else:
        if not K0.is_Exact:
            K0_inexact, K0 = K0, K0.get_exact()
            f = dup_convert(f, K0_inexact, K0)
        else:
            K0_inexact = None

        if K0.is_Field:
            K = K0.get_ring()

            denom, f = dup_clear_denoms(f, K0, K)
            f = dup_convert(f, K0, K)
        else:
            K = K0

        if K.is_ZZ:
            coeff, factors = dup_zz_factor(f, K)
        elif K.is_Poly:
            f, u = dmp_inject(f, 0, K)

            coeff, factors = dmp_factor_list(f, u, K.dom)

            for i, (f, k) in enumerate(factors):
                factors[i] = (dmp_eject(f, u, K), k)

            coeff = K.convert(coeff, K.dom)
        else:  # pragma: no cover
            raise DomainError('factorization not supported over %s' % K0)

        if K0.is_Field:
            for i, (f, k) in enumerate(factors):
                factors[i] = (dup_convert(f, K, K0), k)

            coeff = K0.convert(coeff, K)
            coeff = K0.quo(coeff, denom)

            if K0_inexact:
                for i, (f, k) in enumerate(factors):
                    max_norm = dup_max_norm(f, K0)
                    f = dup_quo_ground(f, max_norm, K0)
                    f = dup_convert(f, K0, K0_inexact)
                    factors[i] = (f, k)
                    coeff = K0.mul(coeff, K0.pow(max_norm, k))

                coeff = K0_inexact.convert(coeff, K0)
                K0 = K0_inexact

    if j:
        factors.insert(0, ([K0.one, K0.zero], j))

    return coeff*cont, _sort_factors(factors)

