
def _poly_roots(poly):
    """Function to get the roots of a polynomial."""
    def _eval(l):
        return [float(i) if i.is_real else complex(i) for i in l]
    if poly.domain in (QQ, ZZ):
        return _eval(poly.all_roots())
    # XXX: Use all_roots() for irrational coefficients when possible
    # See https://github.com/sympy/sympy/issues/22943
    return _eval(poly.nroots())

