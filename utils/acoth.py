
def acoth(ctx, z):
    if not z:
        return ctx.pi * 0.5j
    else:
        return ctx.atanh(ctx.one / z)

