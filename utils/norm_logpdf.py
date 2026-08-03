import math


def norm_logpdf(x, xp=None):
    xp = array_namespace(x) if xp is None else xp
    return -0.5*math.log(2*xp.pi) - x**2/2

