
def ff(ctx, x, n):
    x1 = ctx.fadd(x, 1, prec=2*ctx.prec)
    xn1 = ctx.fadd(ctx.fsub(x, n, prec=2*ctx.prec), 1, prec=2*ctx.prec)
    return ctx.gammaprod([x1], [xn1])

