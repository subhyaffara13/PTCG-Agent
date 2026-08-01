
def dmp_ext_factor(f, u, K):
    r"""Factor multivariate polynomials over algebraic number fields.

    The domain `K` must be an algebraic number field `k(a)` (see :ref:`QQ(a)`).

    Examples
    ========

    First define the algebraic number field `K = \mathbb{Q}(\sqrt{2})`:

    >>> from sympy import QQ, sqrt
    >>> from sympy.polys.factortools import dmp_ext_factor
    >>> K = QQ.algebraic_field(sqrt(2))

    We can now factorise the polynomial `x^2 y^2 - 2` over `K`:

    >>> p = [[K(1),K(0),K(0)], [], [K(-2)]] # x**2*y**2 - 2
    >>> p1 = [[K(1),K(0)], [-K.unit]]       # x*y - sqrt(2)
    >>> p2 = [[K(1),K(0)], [+K.unit]]       # x*y + sqrt(2)
    >>> dmp_ext_factor(p, 1, K) == (K.one, [(p1, 1), (p2, 1)])
    True

    Usually this would be done at a higher level:

    >>> from sympy import factor
    >>> from sympy.abc import x, y
    >>> factor(x**2*y**2 - 2, extension=sqrt(2))
    (x*y - sqrt(2))*(x*y + sqrt(2))

    Explanation
    ===========

    This is Trager's algorithm for multivariate polynomials. In particular this
    function is algorithm ``alg_factor`` from [Trager76]_.

    See :func:`dup_ext_factor` for explanation.

    See Also
    ========

    dup_ext_factor:
        Analogous function for univariate polynomials over ``k(a)``.
    dmp_sqf_norm:
        Multivariate version of subroutine ``sqfr_norm`` also from [Trager76]_.
    sympy.polys.polytools.factor:
        The high-level function that ultimately uses this function as needed.
    """
    if not u:
        return dup_ext_factor(f, K)

    lc = dmp_ground_LC(f, u, K)
    f = dmp_ground_monic(f, u, K)

    if all(d <= 0 for d in dmp_degree_list(f, u)):
        return lc, []

    f, F = dmp_sqf_part(f, u, K), f
    s, g, r = dmp_sqf_norm(f, u, K)

    factors = dmp_factor_list_include(r, u, K.dom)

    if len(factors) == 1:
        factors = [f]
    else:
        for i, (factor, _) in enumerate(factors):
            h = dmp_convert(factor, u, K.dom, K)
            h, _, g = dmp_inner_gcd(h, g, u, K)
            a = [si*K.unit for si in s]
            h = dmp_shift(h, a, u, K)
            factors[i] = h

    result = dmp_trial_division(F, factors, u, K)

    _dmp_check_degrees(F, u, result)

    return lc, result

