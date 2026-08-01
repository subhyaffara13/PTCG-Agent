
def _int_inversion(g, x, t):
    """
    Compute the laplace inversion integral, assuming the formula applies.
    """
    b, a = _get_coeff_exp(g.argument, x)
    C, g = _inflate_fox_h(meijerg(g.an, g.aother, g.bm, g.bother, b/t**a), -a)
    return C/t*g

