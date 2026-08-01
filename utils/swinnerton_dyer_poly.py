
def swinnerton_dyer_poly(n, x=None, polys=False):
    """Generates n-th Swinnerton-Dyer polynomial in `x`.

    Parameters
    ----------
    n : int
        `n` decides the order of polynomial
    x : optional
    polys : bool, optional
        ``polys=True`` returns an expression, otherwise
        (default) returns an expression.
    """
    if n <= 0:
        raise ValueError(
            "Cannot generate Swinnerton-Dyer polynomial of order %s" % n)

    if x is not None:
        sympify(x)
    else:
        x = Dummy('x')

    if n > 3:
        from sympy.functions.elementary.miscellaneous import sqrt
        from .numberfields import minimal_polynomial
        p = 2
        a = [sqrt(2)]
        for i in range(2, n + 1):
            p = nextprime(p)
            a.append(sqrt(p))
        return minimal_polynomial(Add(*a), x, polys=polys)

    if n == 1:
        ex = x**2 - 2
    elif n == 2:
        ex = x**4 - 10*x**2 + 1
    elif n == 3:
        ex = x**8 - 40*x**6 + 352*x**4 - 960*x**2 + 576

    return PurePoly(ex, x) if polys else ex

