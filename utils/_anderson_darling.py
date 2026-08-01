
def _anderson_darling(dist, data, axis):
    x = np.sort(data, axis=-1)
    n = data.shape[-1]
    i = np.arange(1, n+1)
    Si = (2*i - 1)/n * (dist.logcdf(x) + dist.logsf(x[..., ::-1]))
    S = np.sum(Si, axis=-1)
    return -n - S

