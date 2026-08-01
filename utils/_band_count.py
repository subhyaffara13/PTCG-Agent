
def _band_count(a):
    """Returns ml and mu, the lower and upper band sizes of a."""
    nrows, ncols = a.shape
    ml = 0
    for k in range(-nrows+1, 0):
        if np.diag(a, k).any():
            ml = -k
            break
    mu = 0
    for k in range(nrows-1, 0, -1):
        if np.diag(a, k).any():
            mu = k
            break
    return ml, mu

