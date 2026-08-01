
def _ppoly_eval_1(c, x, xps):
    """Evaluate piecewise polynomial manually"""
    out = np.zeros((len(xps), c.shape[2]))
    for i, xp in enumerate(xps):
        if xp < 0 or xp > 1:
            out[i,:] = np.nan
            continue
        j = np.searchsorted(x, xp) - 1
        d = xp - x[j]
        assert x[j] <= xp < x[j+1]
        r = sum(c[k,j] * d**(c.shape[0]-k-1)
                for k in range(c.shape[0]))
        out[i,:] = r
    return out

