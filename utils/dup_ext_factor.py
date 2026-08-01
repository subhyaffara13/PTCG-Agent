
def dup_ext_factor(f, K):
    r"""Factor univariate polynomials over algebraic number fields.

    The domain `K` must be an algebraic number field `k(a)` (see :ref:`QQ(a)`).

    Examples
    ========

    First define the algebraic number field `K = \mathbb{Q}(\sqrt{2})`:

    >>> from sympy import QQ, sqrt
    >>> from sympy.polys.factortools import dup_ext_factor
    >>> K = QQ.algebraic_field(sqrt(2))

    We can now factorise the polynomial `x^2 - 2` over `K`:

    >>> p = [K(1), K(0), K(-2)] # x^2 - 2
    >>> p1 = [K(1), -K.unit]    # x - sqrt(2)
    >>> p2 = [K(1), +K.unit]    # x + sqrt(2)
    >>> dup_ext_factor(p, K) == (K.one, [(p1, 1), (p2, 1)])
    True

    Usually this would be done at a higher level:

    >>> from sympy import factor
    >>> from sympy.abc import x
    >>> factor(x**2 - 2, extension=sqrt(2))
    (x - sqrt(2))*(x + sqrt(2))

    Explanation
    ===========

    Uses Trager's algorithm. In particular this function is algorithm
    ``alg_factor`` from [Trager76]_.

    If `f` is a polynomial in `k(a)[x]` then its norm `g(x)` is a polynomial in
    `k[x]`. If `g(x)` is square-free and has irreducible factors `g_1(x)`,
    `g_2(x)`, `\cdots` then the irreducible factors of `f` in `k(a)[x]` are
    given by `f_i(x) = \gcd(f(x), g_i(x))` where the GCD is computed in
    `k(a)[x]`.

    The first step in Trager's algorithm is to find an integer shift `s` so
    that `f(x-sa)` has square-free norm. Then the norm is factorized in `k[x]`
    and the GCD of (shifted) `f` with each factor gives the shifted factors of
    `f`. At the end the shift is undone to recover the unshifted factors of `f`
    in `k(a)[x]`.

    The algorithm reduces the problem of factorization in `k(a)[x]` to
    factorization in `k[x]` with the main additional steps being to compute the
    norm (a resultant calculation in `k[x,y]`) and some polynomial GCDs in
    `k(a)[x]`.

    In practice in SymPy the base field `k` will be the rationals :ref:`QQ` and
    this function factorizes a polynomial with coefficients in an algebraic
    number field  like `\mathbb{Q}(\sqrt{2})`.

    See Also
    ========

    dmp_ext_factor:
        Analogous function for multivariate polynomials over ``k(a)``.
    dup_sqf_norm:
        Subroutine ``sqfr_norm`` also from [Trager76]_.
    sympy.polys.polytools.factor:
        The high-level function that ultimately uses this function as needed.
    """
    n, lc = dup_degree(f), dup_LC(f, K)

    f = dup_monic(f, K)

    if n <= 0:
        return lc, []
    if n == 1:
        return lc, [(f, 1)]

    f, F = dup_sqf_part(f, K), f
    s, g, r = dup_sqf_norm(f, K)

    factors = dup_factor_list_include(r, K.dom)

    if len(factors) == 1:
        return lc, [(f, n//dup_degree(f))]

    H = s*K.unit

    for i, (factor, _) in enumerate(factors):
        h = dup_convert(factor, K.dom, K)
        h, _, g = dup_inner_gcd(h, g, K)
        h = dup_shift(h, H, K)
        factors[i] = h

    factors = dup_trial_division(F, factors, K)

    _dup_check_degrees(F, factors)

    return lc, factors

