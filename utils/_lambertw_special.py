
def _lambertw_special(ctx, z, k):
    # W(0,0) = 0; all other branches are singular
    if not z:
        if not k:
            return z
        return ctx.ninf + z
    if z == ctx.inf:
        if k == 0:
            return z
        else:
            return z + 2*k*ctx.pi*ctx.j
    if z == ctx.ninf:
        return (-z) + (2*k+1)*ctx.pi*ctx.j
    # Some kind of nan or complex inf/nan?
    return ctx.ln(z)

