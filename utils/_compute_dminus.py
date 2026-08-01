
def _compute_dminus(cdfvals):
    n = cdfvals.shape[-1]
    return (cdfvals - np.arange(0.0, n)/n).max(axis=-1)

