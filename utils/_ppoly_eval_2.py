
def _ppoly_eval_2(coeffs, breaks, xnew, fill=np.nan):
    """Evaluate piecewise polynomial manually (another way)"""
    a = breaks[0]
    b = breaks[-1]
    K = coeffs.shape[0]

    saveshape = np.shape(xnew)
    xnew = np.ravel(xnew)
    res = np.empty_like(xnew)
    mask = (xnew >= a) & (xnew <= b)
    res[~mask] = fill
    xx = xnew.compress(mask)
    indxs = np.searchsorted(breaks, xx)-1
    indxs = indxs.clip(0, len(breaks))
    pp = coeffs
    diff = xx - breaks.take(indxs)
    V = np.vander(diff, N=K)
    values = np.array([np.dot(V[k, :], pp[:, indxs[k]]) for k in range(len(xx))])
    res[mask] = values
    res = res.reshape(saveshape)
    return res

