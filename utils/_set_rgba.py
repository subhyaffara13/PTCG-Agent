
def _set_rgba(ctx, color, alpha, forced_alpha):
    if len(color) == 3 or forced_alpha:
        ctx.set_source_rgba(*color[:3], alpha)
    else:
        ctx.set_source_rgba(*color)

