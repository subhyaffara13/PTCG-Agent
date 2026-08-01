
def TRpower(rv):
    """Convert sin(x)**n and cos(x)**n with positive n to sums.

    Examples
    ========

    >>> from sympy.simplify.fu import TRpower
    >>> from sympy.abc import x
    >>> from sympy import cos, sin
    >>> TRpower(sin(x)**6)
    -15*cos(2*x)/32 + 3*cos(4*x)/16 - cos(6*x)/32 + 5/16
    >>> TRpower(sin(x)**3*cos(2*x)**4)
    (3*sin(x)/4 - sin(3*x)/4)*(cos(4*x)/2 + cos(8*x)/8 + 3/8)

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/List_of_trigonometric_identities#Power-reduction_formulae

    """

    def f(rv):
        if not (isinstance(rv, Pow) and isinstance(rv.base, (sin, cos))):
            return rv
        b, n = rv.as_base_exp()
        x = b.args[0]
        if n.is_Integer and n.is_positive:
            if n.is_odd and isinstance(b, cos):
                rv = 2**(1-n)*Add(*[binomial(n, k)*cos((n - 2*k)*x)
                    for k in range((n + 1)/2)])
            elif n.is_odd and isinstance(b, sin):
                rv = 2**(1-n)*S.NegativeOne**((n-1)/2)*Add(*[binomial(n, k)*
                    S.NegativeOne**k*sin((n - 2*k)*x) for k in range((n + 1)/2)])
            elif n.is_even and isinstance(b, cos):
                rv = 2**(1-n)*Add(*[binomial(n, k)*cos((n - 2*k)*x)
                    for k in range(n/2)])
            elif n.is_even and isinstance(b, sin):
                rv = 2**(1-n)*S.NegativeOne**(n/2)*Add(*[binomial(n, k)*
                    S.NegativeOne**k*cos((n - 2*k)*x) for k in range(n/2)])
            if n.is_even:
                rv += 2**(-n)*binomial(n, n/2)
        return rv

    return bottom_up(rv, f)

