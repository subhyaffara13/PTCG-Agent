
def _iuc(x, y):
    out = np.empty_like(x, dtype=bool)
    nonzero = (y != 0)
    # handles (x, y) = (0, 0) too
    out[~nonzero] = False
    out[nonzero] = (abs(x[nonzero]/y[nonzero]) < 1.0)
    return out

