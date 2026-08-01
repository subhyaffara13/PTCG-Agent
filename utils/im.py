
def im(ctx, x):
    x = ctx.convert(x)
    if hasattr(x, "imag"):    # py2.5 doesn't have .real/.imag for all numbers
        return x.imag
    return ctx.zero

