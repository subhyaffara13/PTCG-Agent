
def laguerre_poly(n, x=None, alpha=0, polys=False):
    r"""Generates the Laguerre polynomial `L_n^{(\alpha)}(x)`.

    Parameters
    ==========

    n : int
        Degree of the polynomial.
    x : optional
    alpha : optional
        Decides minimal domain for the list of coefficients.
    polys : bool, optional
        If True, return a Poly, otherwise (default) return an expression.
    """
    return named_poly(n, dup_laguerre, None, "Laguerre polynomial", (x, alpha), polys)

