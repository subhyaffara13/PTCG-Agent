
def _mpmath_wrightomega(z, dps):
    with mpmath.workdps(dps):
        z = mpmath.mpc(z)
        unwind = mpmath.ceil((z.imag - mpmath.pi)/(2*mpmath.pi))
        res = mpmath.lambertw(mpmath.exp(z), unwind)
    return res

