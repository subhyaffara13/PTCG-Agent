
def _calc_b(data, knots):
    """Calculate lower bbox bound for LSQ splines (mimics f2py calc_b)."""
    val1 = np.min(data)
    val2 = np.min(knots)
    if val2 > val1:
        return val1
    val_max = np.max(knots)
    return val2 - (val_max - val2) / len(knots)

