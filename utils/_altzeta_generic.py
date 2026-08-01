
def _altzeta_generic(ctx, s):
    if s == 1:
        return ctx.ln2 + 0*s
    return -ctx.powm1(2, 1-s) * ctx.zeta(s)

