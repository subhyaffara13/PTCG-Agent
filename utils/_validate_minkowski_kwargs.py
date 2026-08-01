
def _validate_minkowski_kwargs(X, m, n, **kwargs):
    kwargs = _validate_weight_with_size(X, m, n, **kwargs)
    if 'p' not in kwargs:
        kwargs['p'] = 2.
    else:
        if kwargs['p'] <= 0:
            raise ValueError("p must be greater than 0")

    return kwargs

