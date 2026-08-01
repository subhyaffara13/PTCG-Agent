
def make_simp(z):
    """ Create a function that simplifies rational functions in ``z``. """

    def simp(expr):
        """ Efficiently simplify the rational function ``expr``. """
        numer, denom = expr.as_numer_denom()
        numer = numer.expand()
        # denom = denom.expand()  # is this needed?
        c, numer, denom = poly(numer, z).cancel(poly(denom, z))
        return c * numer.as_expr() / denom.as_expr()

    return simp

