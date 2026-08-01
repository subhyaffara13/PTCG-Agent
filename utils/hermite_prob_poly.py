
def hermite_prob_poly(n, x=None, polys=False):
    r"""Generates the probabilist's Hermite polynomial `He_n(x)`.

    Parameters
    ==========

    n : int
        Degree of the polynomial.
    x : optional
    polys : bool, optional
        If True, return a Poly, otherwise (default) return an expression.
    """
    return named_poly(n, dup_hermite_prob, ZZ,
            "probabilist's Hermite polynomial", (x,), polys)

