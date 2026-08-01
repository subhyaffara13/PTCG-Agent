
def hermite_poly(n, x=None, polys=False):
    r"""Generates the Hermite polynomial `H_n(x)`.

    Parameters
    ==========

    n : int
        Degree of the polynomial.
    x : optional
    polys : bool, optional
        If True, return a Poly, otherwise (default) return an expression.
    """
    return named_poly(n, dup_hermite, ZZ, "Hermite polynomial", (x,), polys)

