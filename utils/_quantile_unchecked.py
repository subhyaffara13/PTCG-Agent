
def _quantile_unchecked(a,
                        q,
                        axis=None,
                        out=None,
                        overwrite_input=False,
                        method="linear",
                        keepdims=False,
                        weights=None,
                        weak_q=False):
    """Assumes that q is in [0, 1], and is an ndarray"""
    return _ureduce(a,
                    func=_quantile_ureduce_func,
                    q=q,
                    weights=weights,
                    keepdims=keepdims,
                    axis=axis,
                    out=out,
                    overwrite_input=overwrite_input,
                    method=method,
                    weak_q=weak_q)

