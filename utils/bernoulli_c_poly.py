
def bernoulli_c_poly(n, x=None, polys=False):
    r"""Generates the central Bernoulli polynomial `\operatorname{B}_n^c(x)`.

    These are scaled and shifted versions of the plain Bernoulli polynomials,
    done in such a way that `\operatorname{B}_n^c(x)` is an even or odd function
    for even or odd `n` respectively:

    .. math :: \operatorname{B}_n^c(x) = 2^n \operatorname{B}_n
            \left(\frac{x+1}{2}\right)

    Parameters
    ==========

    n : int
        Degree of the polynomial.
    x : optional
    polys : bool, optional
        If True, return a Poly, otherwise (default) return an expression.
    """
    return named_poly(n, dup_bernoulli_c, QQ, "central Bernoulli polynomial", (x,), polys)

