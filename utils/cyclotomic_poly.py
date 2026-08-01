
def cyclotomic_poly(n, x=None, polys=False):
    """Generates cyclotomic polynomial of order `n` in `x`.

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
            "Cannot generate cyclotomic polynomial of order %s" % n)

    poly = DMP(dup_zz_cyclotomic_poly(int(n), ZZ), ZZ)

    if x is not None:
        poly = Poly.new(poly, x)
    else:
        poly = PurePoly.new(poly, Dummy('x'))

    return poly if polys else poly.as_expr()

