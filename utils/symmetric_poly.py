
def symmetric_poly(n, *gens, polys=False):
    """
    Generates symmetric polynomial of order `n`.

    Parameters
    ==========

    polys: bool, optional (default: False)
        Returns a Poly object when ``polys=True``, otherwise
        (default) returns an expression.
    """
    gens = _analyze_gens(gens)

    if n < 0 or n > len(gens) or not gens:
        raise ValueError("Cannot generate symmetric polynomial of order %s for %s" % (n, gens))
    elif not n:
        poly = S.One
    else:
        poly = Add(*[Mul(*s) for s in subsets(gens, int(n))])

    return Poly(poly, *gens) if polys else poly

