
def _rhp(x, y):
    out = np.empty_like(x, dtype=bool)
    nonzero = (y != 0)
    # handles (x, y) = (0, 0) too
    out[~nonzero] = False
    out[nonzero] = (np.real(x[nonzero]/y[nonzero]) > 0.0)
    return out

