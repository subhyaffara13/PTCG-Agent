import math


def _pow10m1(x):
    """10 ** x - 1 for x near 0"""
    return math.expm1(_POW10_LOG10 * x)

