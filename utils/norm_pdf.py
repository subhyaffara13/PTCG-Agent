
def norm_pdf(x, xp=None):
    xp = array_namespace(x) if xp is None else xp
    return 1/(2*xp.pi)**0.5 * xp.exp(-x**2/2)

