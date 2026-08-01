
def pcfw(ctx, a, z, **kwargs):
    r"""
    Gives the parabolic cylinder function `W(a,z)` defined in (DLMF 12.14).

    **Examples**

    Value at the origin::

        >>> from mpmath import *
        >>> mp.dps = 25; mp.pretty = True
        >>> a = mpf(0.25)
        >>> pcfw(a,0)
        0.9722833245718180765617104
        >>> power(2,-0.75)*sqrt(abs(gamma(0.25+0.5j*a)/gamma(0.75+0.5j*a)))
        0.9722833245718180765617104
        >>> diff(pcfw,(a,0),(0,1))
        -0.5142533944210078966003624
        >>> -power(2,-0.25)*sqrt(abs(gamma(0.75+0.5j*a)/gamma(0.25+0.5j*a)))
        -0.5142533944210078966003624

    """
    n, _ = ctx._convert_param(a)
    z = ctx.convert(z)
    def terms():
        phi2 = ctx.arg(ctx.gamma(0.5 + ctx.j*n))
        phi2 = (ctx.loggamma(0.5+ctx.j*n) - ctx.loggamma(0.5-ctx.j*n))/2j
        rho = ctx.pi/8 + 0.5*phi2
        # XXX: cancellation computing k
        k = ctx.sqrt(1 + ctx.exp(2*ctx.pi*n)) - ctx.exp(ctx.pi*n)
        C = ctx.sqrt(k/2) * ctx.exp(0.25*ctx.pi*n)
        yield C * ctx.expj(rho) * ctx.pcfu(ctx.j*n, z*ctx.expjpi(-0.25))
        yield C * ctx.expj(-rho) * ctx.pcfu(-ctx.j*n, z*ctx.expjpi(0.25))
    v = ctx.sum_accurately(terms)
    if ctx._is_real_type(n) and ctx._is_real_type(z):
        v = ctx._re(v)
    return v

