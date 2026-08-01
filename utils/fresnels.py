
def fresnels(ctx, z):
    if z == ctx.inf:
        return ctx.mpf(0.5)
    if z == ctx.ninf:
        return ctx.mpf(-0.5)
    return ctx.pi*z**3/6*ctx.hyp1f2((3,4),(3,2),(7,4),-ctx.pi**2*z**4/16)

