
def shi(ctx, z):
    # Suffers from cancellation near 0
    if ctx.mag(z) >= -1:
        nz = ctx.fneg(z, exact=True)
        v = 0.5*(ctx.ei(z) - ctx.ei(nz))
        zimag = ctx._im(z)
        if zimag > 0: v -= 0.5j*ctx.pi
        if zimag < 0: v += 0.5j*ctx.pi
        return v
    else:
        return z * ctx.hyp1f2((1,2),(3,2),(3,2),0.25*z*z)

