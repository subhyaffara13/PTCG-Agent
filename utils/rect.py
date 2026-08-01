
def rect(ctx, r, phi):
    return r * ctx.mpc(*ctx.cos_sin(phi))

