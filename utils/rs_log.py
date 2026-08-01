
def rs_log(p, x, prec):
    """
    The Logarithm of ``p`` modulo ``O(x**prec)``.

    Notes
    =====

    Truncation of ``integral dx p**-1*d p/dx`` is used.

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.puiseux import puiseux_ring
    >>> from sympy.polys.ring_series import rs_log
    >>> R, x = puiseux_ring('x', QQ)
    >>> rs_log(1 + x, x, 8)
    x + -1/2*x**2 + 1/3*x**3 + -1/4*x**4 + 1/5*x**5 + -1/6*x**6 + 1/7*x**7
    >>> rs_log(x**QQ(3, 2) + 1, x, 5)
    x**(3/2) + -1/2*x**3 + 1/3*x**(9/2)
    """
    if rs_is_puiseux(p, x):
        return rs_puiseux(rs_log, p, x, prec)
    R = p.ring
    if p == 1:
        return R.zero
    c = _get_constant_term(p, x)
    if c:
        const = 0
        if c == 1:
            pass
        try:
            c_expr = c.as_expr()
            const = R(log(c_expr))
        except ValueError:
            R = R.add_gens([log(c_expr)])
            p = p.set_ring(R)
            x = x.set_ring(R)
            c = c.set_ring(R)
            const = R(log(c_expr))

        dlog = p.diff(x)
        dlog = rs_mul(dlog, _series_inversion1(p, x, prec), x, prec - 1)
        return rs_integrate(dlog, x) + const
    else:
        raise NotImplementedError

