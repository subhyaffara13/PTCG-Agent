
def _quantile_ureduce_func(
    a: np.ndarray,
    q: np.ndarray,
    weights: np.ndarray | None,
    axis: int | None = None,
    out: np.ndarray | None = None,
    overwrite_input: bool = False,
    method: str = "linear",
    weak_q: bool = False,
) -> np.ndarray:
    if q.ndim > 2:
        # The code below works fine for nd, but it might not have useful
        # semantics. For now, keep the supported dimensions the same as it was
        # before.
        raise ValueError("q must be a scalar or 1d")
    if overwrite_input:
        if axis is None:
            axis = 0
            arr = a.ravel()
            wgt = None if weights is None else weights.ravel()
        else:
            arr = a
            wgt = weights
    elif axis is None:
        axis = 0
        arr = a.flatten()
        wgt = None if weights is None else weights.flatten()
    else:
        arr = a.copy()
        wgt = weights
    result = _quantile(arr,
                       quantiles=q,
                       axis=axis,
                       method=method,
                       out=out,
                       weights=wgt,
                       weak_q=weak_q)
    return result

