
def fresnelc(ctx, z):
    if z == ctx.inf:
        return ctx.mpf(0.5)
    if z == ctx.ninf:
        return ctx.mpf(-0.5)
    return z*ctx.hyp1f2((1,4),(1,2),(5,4),-ctx.pi**2*z**4/16)

