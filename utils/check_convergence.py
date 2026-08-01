
def check_convergence(numer: Expr, denom: Expr, n: Symbol) -> tuple[int, Any, Any]:
    """
    Returns
    =======

    (h, g, p) where
    -- h is:
        > 0 for convergence of rate 1/factorial(n)**h
        < 0 for divergence of rate factorial(n)**(-h)
        = 0 for geometric or polynomial convergence or divergence

    -- abs(g) is:
        > 1 for geometric convergence of rate 1/h**n
        < 1 for geometric divergence of rate h**n
        = 1 for polynomial convergence or divergence

        (g < 0 indicates an alternating series)

    -- p is:
        > 1 for polynomial convergence of rate 1/n**h
        <= 1 for polynomial divergence of rate n**(-h)

    """
    from sympy.polys.polytools import Poly
    npol = Poly(numer, n)
    dpol = Poly(denom, n)
    p = npol.degree()
    q = dpol.degree()
    rate = q - p
    if rate:
        return rate, None, None
    constant = dpol.LC() / npol.LC()
    from .numbers import equal_valued
    if not equal_valued(abs(constant), 1):
        return rate, constant, None
    if npol.degree() == dpol.degree() == 0:
        return rate, constant, 0
    pc = npol.all_coeffs()[1]
    qc = dpol.all_coeffs()[1]
    return rate, constant, (qc - pc)/dpol.LC()

