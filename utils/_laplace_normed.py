
def _laplace_normed(m, d, nd):
    laplace = _laplace(m, d)
    return lambda v: nd[:, np.newaxis] * laplace(v * nd[:, np.newaxis])

