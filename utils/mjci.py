
def mjci(data, prob=(0.25, 0.5, 0.75), axis=None):
    """
    Returns the Maritz-Jarrett estimators of the standard error of selected
    experimental quantiles of the data.

    Parameters
    ----------
    data : ndarray
        Data array.
    prob : sequence, optional
        Sequence of quantiles to compute.
    axis : int or None, optional
        Axis along which to compute the quantiles. If None, use a flattened
        array.

    """  # numpydoc ignore=RT01
    def _mjci_1D(data, p):
        data = np.sort(data.compressed())
        n = data.size
        prob = (np.array(p) * n + 0.5).astype(int)
        betacdf = beta.cdf

        mj = np.empty(len(prob), float64)
        x = np.arange(1,n+1, dtype=float64) / n
        y = x - 1./n
        for (i,m) in enumerate(prob):
            W = betacdf(x,m-1,n-m) - betacdf(y,m-1,n-m)
            C1 = np.dot(W,data)
            C2 = np.dot(W,data**2)
            mj[i] = np.sqrt(C2 - C1**2)
        return mj

    data = ma.array(data, copy=False)
    if data.ndim > 2:
        raise ValueError(f"Array 'data' must be at most two dimensional, "
                         f"but got data.ndim = {data.ndim}")

    p = np.atleast_1d(np.asarray(prob))
    # Computes quantiles along axis (or globally)
    if (axis is None):
        return _mjci_1D(data, p)
    else:
        return ma.apply_along_axis(_mjci_1D, axis, data, p)

