
def re(ctx, x):
    x = ctx.convert(x)
    if hasattr(x, "real"):    # py2.5 doesn't have .real/.imag for all numbers
        return x.real
    return x

