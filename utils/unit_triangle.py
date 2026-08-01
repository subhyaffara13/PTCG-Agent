
def unit_triangle(ctx, t, amplitude=1):
    A = amplitude
    if t <= -1 or t >= 1:
        return ctx.zero
    return A*(-ctx.fabs(t) + 1)

