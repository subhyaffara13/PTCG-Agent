
def randcplx(offset=-1):
    """ Polys is not good with real coefficients. """
    return _randrat() + I*_randrat() + I*(1 + offset)

