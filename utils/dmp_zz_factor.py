
def dmp_zz_factor(f, u, K):
    r"""
    Factor (non square-free) polynomials in `Z[X]`.

    Given a multivariate polynomial `f` in `Z[x]` computes its complete
    factorization `f_1, \dots, f_n` into irreducibles over integers::

                 f = content(f) f_1**k_1 ... f_n**k_n

    The factorization is computed by reducing the input polynomial
    into a primitive square-free polynomial and factoring it using
    Enhanced Extended Zassenhaus (EEZ) algorithm. Trial division
    is used to recover the multiplicities of factors.

    The result is returned as a tuple consisting of::

             (content(f), [(f_1, k_1), ..., (f_n, k_n))

    Consider polynomial `f = 2*(x**2 - y**2)`::

        >>> from sympy.polys import ring, ZZ
        >>> R, x,y = ring("x,y", ZZ)

        >>> R.dmp_zz_factor(2*x**2 - 2*y**2)
        (2, [(x - y, 1), (x + y, 1)])

    In result we got the following factorization::

                    f = 2 (x - y) (x + y)

    References
    ==========

    .. [1] [Gathen99]_

    """
    if not u:
        return dup_zz_factor(f, K)

    if dmp_zero_p(f, u):
        return K.zero, []

    cont, g = dmp_ground_primitive(f, u, K)

    if dmp_ground_LC(g, u, K) < 0:
        cont, g = -cont, dmp_neg(g, u, K)

    if all(d <= 0 for d in dmp_degree_list(g, u)):
        return cont, []

    G, g = dmp_primitive(g, u, K)

    factors = []

    if dmp_degree(g, u) > 0:
        g = dmp_sqf_part(g, u, K)
        H = dmp_zz_wang(g, u, K)
        factors = dmp_trial_division(f, H, u, K)

    for g, k in dmp_zz_factor(G, u - 1, K)[1]:
        factors.insert(0, ([g], k))

    _dmp_check_degrees(f, u, factors)

    return cont, _sort_factors(factors)

