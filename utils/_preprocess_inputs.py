
def _preprocess_inputs(k, t_tpl):
    """Helpers: validate and preprocess NdBSpline inputs.

       Parameters
       ----------
       k : int or tuple
          Spline orders
       t_tpl : tuple or array-likes
          Knots.
    """
    # 1. Make sure t_tpl is a tuple
    if not isinstance(t_tpl, tuple):
        raise ValueError(f"Expect `t` to be a tuple of array-likes. "
                         f"Got {t_tpl} instead."
        )

    # 2. Make ``k`` a tuple of integers
    ndim = len(t_tpl)
    try:
        len(k)
    except TypeError:
        # make k a tuple
        k = (k,)*ndim

    k = np.asarray([operator.index(ki) for ki in k], dtype=np.int64)

    if len(k) != ndim:
        raise ValueError(f"len(t) = {len(t_tpl)} != {len(k) = }.")

    # 3. Validate inputs
    ndim = len(t_tpl)
    for d in range(ndim):
        td = np.asarray(t_tpl[d])
        kd = k[d]
        n = td.shape[0] - kd - 1
        if kd < 0:
            raise ValueError(f"Spline degree in dimension {d} cannot be"
                             f" negative.")
        if td.ndim != 1:
            raise ValueError(f"Knot vector in dimension {d} must be"
                             f" one-dimensional.")
        if n < kd + 1:
            raise ValueError(f"Need at least {2*kd + 2} knots for degree"
                             f" {kd} in dimension {d}.")
        if (np.diff(td) < 0).any():
            raise ValueError(f"Knots in dimension {d} must be in a"
                             f" non-decreasing order.")
        if len(np.unique(td[kd:n + 1])) < 2:
            raise ValueError(f"Need at least two internal knots in"
                             f" dimension {d}.")
        if not np.isfinite(td).all():
            raise ValueError(f"Knots in dimension {d} should not have"
                             f" nans or infs.")

    # 4. tabulate the flat indices for iterating over the (k+1)**ndim subarray
    # non-zero b-spline elements
    shape = tuple(kd + 1 for kd in k)
    indices = np.unravel_index(np.arange(prod(shape)), shape)
    _indices_k1d = np.asarray(indices, dtype=np.int64).T.copy()

    # 5. pack the knots into a single array:
    #    ([1, 2, 3, 4], [5, 6], (7, 8, 9)) -->
    #    array([[1, 2, 3, 4],
    #           [5, 6, nan, nan],
    #           [7, 8, 9, nan]])
    t_tpl = [np.asarray(t) for t in t_tpl]
    ndim = len(t_tpl)
    len_t = [len(ti) for ti in t_tpl]
    _t = np.empty((ndim, max(len_t)), dtype=float)
    _t.fill(np.nan)
    for d in range(ndim):
        _t[d, :len(t_tpl[d])] = t_tpl[d]
    len_t = np.asarray(len_t, dtype=np.int64)

    return k, _indices_k1d, (_t, len_t)

