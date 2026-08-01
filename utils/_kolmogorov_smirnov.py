
def _kolmogorov_smirnov(dist, data, axis=-1):
    x = np.sort(data, axis=axis)
    cdfvals = dist.cdf(x)
    cdfvals = np.moveaxis(cdfvals, axis, -1)
    Dplus = _compute_dplus(cdfvals)  # always works along last axis
    Dminus = _compute_dminus(cdfvals)
    return np.maximum(Dplus, Dminus)

