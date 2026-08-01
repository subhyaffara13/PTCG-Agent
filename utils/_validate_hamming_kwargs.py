
def _validate_hamming_kwargs(X, m, n, **kwargs):
    w = kwargs.get('w', np.ones((n,), dtype='double'))

    if w.ndim != 1 or w.shape[0] != n:
        raise ValueError(f"Weights must have same size as input vector. "
                         f"{w.shape[0]} vs. {n}")

    kwargs['w'] = _validate_weights(w)
    return kwargs

