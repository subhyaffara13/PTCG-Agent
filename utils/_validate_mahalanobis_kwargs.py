
def _validate_mahalanobis_kwargs(X, m, n, **kwargs):
    VI = kwargs.pop('VI', None)
    if VI is None:
        if m <= n:
            # There are fewer observations than the dimension of
            # the observations.
            raise ValueError(
                f"The number of observations ({m}) is too small; "
                f"the covariance matrix is singular. For observations "
                f"with {n} dimensions, at least {n + 1} observations are required.")
        if isinstance(X, tuple):
            X = np.vstack(X)
        CV = np.atleast_2d(np.cov(X.astype(np.float64, copy=False).T))
        VI = np.linalg.inv(CV).T.copy()
    kwargs["VI"] = _convert_to_double(VI)
    return kwargs

