
def _apply_scale(sol, scale):
    return [(res, cond / scale) for res, cond in sol]

