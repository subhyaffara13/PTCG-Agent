
def _validate_weight_with_size(X, m, n, **kwargs):
    w = kwargs.pop('w', None)
    if w is None:
        return kwargs

    if w.ndim != 1 or w.shape[0] != n:
        raise ValueError("Weights must have same size as input vector. "
                         f"{w.shape[0]} vs. {n}")

    kwargs['w'] = _validate_weights(w)
    return kwargs

