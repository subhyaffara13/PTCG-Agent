
def sdm_strip(f):
    """Remove terms with zero coefficients from ``f`` in ``K[X]``. """
    return [ (monom, coeff) for monom, coeff in f if coeff ]

