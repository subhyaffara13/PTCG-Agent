
def rs_exp(p, x, prec):
    """
    Exponentiation of a series modulo ``O(x**prec)``

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.rings import ring
    >>> from sympy.polys.ring_series import rs_exp
    >>> R, x = ring('x', QQ)
    >>> rs_exp(x**2, x, 7)
    1/6*x**6 + 1/2*x**4 + x**2 + 1
    """
    if rs_is_puiseux(p, x):
        return rs_puiseux(rs_exp, p, x, prec)
    R = p.ring
    c = _get_constant_term(p, x)
    if c:
        try:
            c_expr = c.as_expr()
            const = R(exp(c_expr))
        except ValueError:
            R = R.add_gens([exp(c_expr)])
            p = p.set_ring(R)
            x = x.set_ring(R)
            c = c.set_ring(R)
            const = R(exp(c_expr))

        p1 = p - c

    # Makes use of SymPy functions to evaluate the values of the cos/sin
    # of the constant term.
        return const*rs_exp(p1, x, prec)

    if len(p) > 20:
        return _exp1(p, x, prec)
    one = R(1)
    n = 1
    c = []
    for k in range(prec):
        c.append(one/n)
        k += 1
        n *= k

    r = rs_series_from_list(p, c, x, prec)
    return r

