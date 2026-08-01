
def dg_series(z, n):
    """Symbolic expansion of digamma(z) in z=0 to order n.

    See https://dlmf.nist.gov/5.7.E4 and with https://dlmf.nist.gov/5.5.E2
    """
    k = symbols("k")
    return -1/z - EulerGamma + \
        sympy.summation((-1)**k * zeta(k) * z**(k-1), (k, 2, n+1))

