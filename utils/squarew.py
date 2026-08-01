
def squarew(ctx, t, amplitude=1, period=1):
    P = period
    A = amplitude
    return A*((-1)**ctx.floor(2*t/P))

