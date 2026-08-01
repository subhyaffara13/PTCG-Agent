
def jacobi_poly(n, a, b, x=None, polys=False):
    r"""Generates the Jacobi polynomial `P_n^{(a,b)}(x)`.

    Parameters
    ==========

    n : int
        Degree of the polynomial.
    a
        Lower limit of minimal domain for the list of coefficients.
    b
        Upper limit of minimal domain for the list of coefficients.
    x : optional
    polys : bool, optional
        If True, return a Poly, otherwise (default) return an expression.
    """
    return named_poly(n, dup_jacobi, None, "Jacobi polynomial", (x, a, b), polys)

