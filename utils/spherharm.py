
def spherharm(ctx, l, m, theta, phi, **kwargs):
    l = ctx.convert(l)
    m = ctx.convert(m)
    theta = ctx.convert(theta)
    phi = ctx.convert(phi)
    l_isint = ctx.isint(l)
    l_natural = l_isint and l >= 0
    m_isint = ctx.isint(m)
    if l_isint and l < 0 and m_isint:
        return ctx.spherharm(-(l+1), m, theta, phi, **kwargs)
    if theta == 0 and m_isint and m < 0:
        return ctx.zero * 1j
    if l_natural and m_isint:
        if abs(m) > l:
            return ctx.zero * 1j
        # http://functions.wolfram.com/Polynomials/
        #     SphericalHarmonicY/26/01/02/0004/
        def h(l,m):
            absm = abs(m)
            C = [-1, ctx.expj(m*phi),
                 (2*l+1)*ctx.fac(l+absm)/ctx.pi/ctx.fac(l-absm),
                 ctx.sin(theta)**2,
                 ctx.fac(absm), 2]
            P = [0.5*m*(ctx.sign(m)+1), 1, 0.5, 0.5*absm, -1, -absm-1]
            return ((C, P, [], [], [absm-l, l+absm+1], [absm+1],
                ctx.sin(0.5*theta)**2),)
    else:
        # http://functions.wolfram.com/HypergeometricFunctions/
        #     SphericalHarmonicYGeneral/26/01/02/0001/
        def h(l,m):
            if ctx.isnpint(l-m+1) or ctx.isnpint(l+m+1) or ctx.isnpint(1-m):
                return (([0], [-1], [], [], [], [], 0),)
            cos, sin = ctx.cos_sin(0.5*theta)
            C = [0.5*ctx.expj(m*phi), (2*l+1)/ctx.pi,
                 ctx.gamma(l-m+1), ctx.gamma(l+m+1),
                 cos**2, sin**2]
            P = [1, 0.5, 0.5, -0.5, 0.5*m, -0.5*m]
            return ((C, P, [], [1-m], [-l,l+1], [1-m], sin**2),)
    return ctx.hypercomb(h, [l,m], **kwargs)

