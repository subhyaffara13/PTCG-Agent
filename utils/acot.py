
def acot(ctx, z):
    if not z:
        return ctx.pi * 0.5
    else:
        return ctx.atan(ctx.one / z)

