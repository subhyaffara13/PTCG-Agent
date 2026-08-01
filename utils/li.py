
def li(ctx, z, offset=False):
    if offset:
        if z == 2:
            return ctx.zero
        return ctx.ei(ctx.ln(z)) - ctx.ei(ctx.ln2)
    if not z:
        return z
    if z == 1:
        return ctx.ninf
    return ctx.ei(ctx.ln(z))

