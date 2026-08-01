
def _compute_dplus(cdfvals):  # adapted from _stats_py before gh-17062
    n = cdfvals.shape[-1]
    return (np.arange(1.0, n + 1) / n - cdfvals).max(axis=-1)

