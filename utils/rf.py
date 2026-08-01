
def rf(ctx, x, n):
    xn = ctx.fadd(x, n, prec=2*ctx.prec)
    return ctx.gammaprod([xn], [x])

