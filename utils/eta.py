
def eta(lam):
    """Function from DLMF 8.12.1 shifted to be centered at 0."""
    if lam > 0:
        return mp.sqrt(2*(lam - mp.log(lam + 1)))
    elif lam < 0:
        return -mp.sqrt(2*(lam - mp.log(lam + 1)))
    else:
        return 0


def eta(ctx, tau):
    r"""
    Returns the Dedekind eta function of tau in the upper half-plane.

        >>> from mpmath import *
        >>> mp.dps = 25; mp.pretty = True
        >>> eta(1j); gamma(0.25) / (2*pi**0.75)
        (0.7682254223260566590025942 + 0.0j)
        0.7682254223260566590025942
        >>> tau = sqrt(2) + sqrt(5)*1j
        >>> eta(-1/tau); sqrt(-1j*tau) * eta(tau)
        (0.9022859908439376463573294 + 0.07985093673948098408048575j)
        (0.9022859908439376463573295 + 0.07985093673948098408048575j)
        >>> eta(tau+1); exp(pi*1j/12) * eta(tau)
        (0.4493066139717553786223114 + 0.3290014793877986663915939j)
        (0.4493066139717553786223114 + 0.3290014793877986663915939j)
        >>> f = lambda z: diff(eta, z) / eta(z)
        >>> chop(36*diff(f,tau)**2 - 24*diff(f,tau,2)*f(tau) + diff(f,tau,3))
        0.0

    """
    if ctx.im(tau) <= 0.0:
        raise ValueError("eta is only defined in the upper half-plane")
    q = ctx.expjpi(tau/12)
    return q * ctx.qp(q**24)

