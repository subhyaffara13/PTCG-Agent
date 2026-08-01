
def _validate_seuclidean_kwargs(X, m, n, **kwargs):
    V = kwargs.pop('V', None)
    if V is None:
        if isinstance(X, tuple):
            X = np.vstack(X)
        V = np.var(X.astype(np.float64, copy=False), axis=0, ddof=1)
    else:
        V = np.asarray(V, order='c')
        if len(V.shape) != 1:
            raise ValueError('Variance vector V must '
                             'be one-dimensional.')
        if V.shape[0] != n:
            raise ValueError('Variance vector V must be of the same '
                             'dimension as the vectors on which the distances '
                             'are computed.')
    kwargs['V'] = _convert_to_double(V)
    return kwargs

