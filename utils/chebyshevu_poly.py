
def chebyshevu_poly(n, x=None, polys=False):
    r"""Generates the Chebyshev polynomial of the second kind `U_n(x)`.

    Parameters
    ==========

    n : int
        Degree of the polynomial.
    x : optional
    polys : bool, optional
        If True, return a Poly, otherwise (default) return an expression.
    """
    return named_poly(n, dup_chebyshevu, ZZ,
            "Chebyshev polynomial of the second kind", (x,), polys)

