
def legendre_poly(n, x=None, polys=False):
    r"""Generates the Legendre polynomial `P_n(x)`.

    Parameters
    ==========

    n : int
        Degree of the polynomial.
    x : optional
    polys : bool, optional
        If True, return a Poly, otherwise (default) return an expression.
    """
    return named_poly(n, dup_legendre, QQ, "Legendre polynomial", (x,), polys)

