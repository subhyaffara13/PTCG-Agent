
def taufrom(ctx, q=None, m=None, k=None, tau=None, qbar=None):
    r"""
    Returns the elliptic half-period ratio `\tau`, given any of
    `q, m, k, \tau, \bar{q}`::

        >>> from mpmath import *
        >>> mp.dps = 25; mp.pretty = True
        >>> taufrom(tau=0.5j)
        (0.0 + 0.5j)
        >>> taufrom(q=qfrom(tau=0.5j))
        (0.0 + 0.5j)
        >>> taufrom(m=mfrom(tau=0.5j))
        (0.0 + 0.5j)
        >>> taufrom(k=kfrom(tau=0.5j))
        (0.0 + 0.5j)
        >>> taufrom(qbar=qbarfrom(tau=0.5j))
        (0.0 + 0.5j)

    """
    if tau is not None:
        return ctx.convert(tau)
    if m is not None:
        m = ctx.convert(m)
        return ctx.j*ctx.ellipk(1-m)/ctx.ellipk(m)
    if k is not None:
        k = ctx.convert(k)
        return ctx.j*ctx.ellipk(1-k**2)/ctx.ellipk(k**2)
    if q is not None:
        return ctx.log(q) / (ctx.pi*ctx.j)
    if qbar is not None:
        qbar = ctx.convert(qbar)
        return ctx.log(qbar) / (2*ctx.pi*ctx.j)

