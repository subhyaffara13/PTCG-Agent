
def _calc_e(data, knots):
    """Calculate upper bbox bound for LSQ splines (mimics f2py calc_e)."""
    val1 = np.max(data)
    val2 = np.max(knots)
    if val2 < val1:
        return val1
    val_min = np.min(knots)
    return val2 + (val2 - val_min) / len(knots)

