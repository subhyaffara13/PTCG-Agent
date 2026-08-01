
def _pdist_callable(X, *, out, metric, **kwargs):
    n = X.shape[0]
    out_size = (n * (n - 1)) // 2
    dm = _prepare_out_argument(out, np.float64, (out_size,))
    k = 0
    for i in range(X.shape[0] - 1):
        for j in range(i + 1, X.shape[0]):
            dm[k] = metric(X[i], X[j], **kwargs)
            k += 1
    return dm

