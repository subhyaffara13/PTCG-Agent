
def _ouc(x, y):
    out = np.empty_like(x, dtype=bool)
    xzero = (x == 0)
    yzero = (y == 0)
    out[xzero & yzero] = False
    out[~xzero & yzero] = True
    out[~yzero] = (abs(x[~yzero]/y[~yzero]) > 1.0)
    return out

