
def as_poly_1t(p, t, z):
    """
    (Hackish) way to convert an element ``p`` of K[t, 1/t] to K[t, z].

    In other words, ``z == 1/t`` will be a dummy variable that Poly can handle
    better.

    See issue 5131.

    Examples
    ========

    >>> from sympy import random_poly
    >>> from sympy.integrals.risch import as_poly_1t
    >>> from sympy.abc import x, z

    >>> p1 = random_poly(x, 10, -10, 10)
    >>> p2 = random_poly(x, 10, -10, 10)
    >>> p = p1 + p2.subs(x, 1/x)
    >>> as_poly_1t(p, x, z).as_expr().subs(z, 1/x) == p
    True
    """
    # TODO: Use this on the final result.  That way, we can avoid answers like
    # (...)*exp(-x).
    pa, pd = frac_in(p, t, cancel=True)
    if not pd.is_monomial:
        # XXX: Is there a better Poly exception that we could raise here?
        # Either way, if you see this (from the Risch Algorithm) it indicates
        # a bug.
        raise PolynomialError("%s is not an element of K[%s, 1/%s]." % (p, t, t))

    t_part, remainder = pa.div(pd)

    ans = t_part.as_poly(t, z, expand=False)

    if remainder:
        one = remainder.one
        tp = t*one
        r = pd.degree() - remainder.degree()
        z_part = remainder.transform(one, tp) * tp**r
        z_part = z_part.replace(t, z).to_field().quo_ground(pd.LC())
        ans += z_part.as_poly(t, z, expand=False)

    return ans

