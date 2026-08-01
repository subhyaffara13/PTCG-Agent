
def _minimal_polynomial_sq(p, n, x):
    """
    Returns the minimal polynomial for the ``nth-root`` of a sum of surds
    or ``None`` if it fails.

    Parameters
    ==========

    p : sum of surds
    n : positive integer
    x : variable of the returned polynomial

    Examples
    ========

    >>> from sympy.polys.numberfields.minpoly import _minimal_polynomial_sq
    >>> from sympy import sqrt
    >>> from sympy.abc import x
    >>> q = 1 + sqrt(2) + sqrt(3)
    >>> _minimal_polynomial_sq(q, 3, x)
    x**12 - 4*x**9 - 4*x**6 + 16*x**3 - 8

    """
    p = sympify(p)
    n = sympify(n)
    if not n.is_Integer or not n > 0 or not _is_sum_surds(p):
        return None
    pn = p**Rational(1, n)
    # eliminate the square roots
    p -= x
    while 1:
        p1 = _separate_sq(p)
        if p1 is p:
            p = p1.subs({x:x**n})
            break
        else:
            p = p1

    # _separate_sq eliminates field extensions in a minimal way, so that
    # if n = 1 then `p = constant*(minimal_polynomial(p))`
    # if n > 1 it contains the minimal polynomial as a factor.
    if n == 1:
        p1 = Poly(p)
        if p.coeff(x**p1.degree(x)) < 0:
            p = -p
        p = p.primitive()[1]
        return p
    # by construction `p` has root `pn`
    # the minimal polynomial is the factor vanishing in x = pn
    factors = factor_list(p)[1]

    result = _choose_factor(factors, x, pn)
    return result

