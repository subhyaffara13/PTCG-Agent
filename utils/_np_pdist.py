
def _np_pdist(X, out, w, V, VI, metric='euclidean', **kwargs):

    X = _asarray_validated(X, sparse_ok=False, objects_ok=True, mask_ok=True,
                           check_finite=False)
    m, n = X.shape

    if w is not None:
        kwargs["w"] = w
    if V is not None:
        kwargs["V"] = V
    if VI is not None:
        kwargs["VI"] = VI

    if callable(metric):
        mstr = getattr(metric, '__name__', 'UnknownCustomMetric')
        metric_info = _METRIC_ALIAS.get(mstr, None)

        if metric_info is not None:
            X, typ, kwargs = _validate_pdist_input(
                X, m, n, metric_info, **kwargs)

        return _pdist_callable(X, metric=metric, out=out, **kwargs)
    elif isinstance(metric, str):
        mstr = metric.lower()
        metric_info = _METRIC_ALIAS.get(mstr, None)

        if metric_info is not None:
            pdist_fn = metric_info.pdist_func
            return pdist_fn(X, out=out, **kwargs)
        elif mstr.startswith("test_"):
            metric_info = _TEST_METRICS.get(mstr, None)
            if metric_info is None:
                raise ValueError(f'Unknown "Test" Distance Metric: {mstr[5:]}')
            X, typ, kwargs = _validate_pdist_input(
                X, m, n, metric_info, **kwargs)
            return _pdist_callable(
                X, metric=metric_info.dist_func, out=out, **kwargs)
        else:
            raise ValueError(f'Unknown Distance Metric: {mstr}')
    else:
        raise TypeError('2nd argument metric must be a string identifier '
                        'or a function.')

