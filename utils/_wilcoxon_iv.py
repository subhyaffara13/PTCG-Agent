
def _wilcoxon_iv(x, y, zero_method, correction, alternative, method, axis):
    xp = array_namespace(x, y)
    x, y = xp_promote(x, y, force_floating=True, xp=xp)

    axis = np.asarray(axis)[()]  # OK to use NumPy for input validation
    message = "`axis` must be an integer."
    if not np.issubdtype(axis.dtype, np.integer) or axis.ndim != 0:
        raise ValueError(message)
    axis = int(axis)

    message = '`axis` must be compatible with the shape(s) of `x` (and `y`)'
    AxisError = getattr(np, 'AxisError', None) or np.exceptions.AxisError
    try:
        if y is None:
            d = x
        else:
            x, y = _broadcast_arrays((x, y), axis=axis, xp=xp)
            d = x - y
        d = xp.moveaxis(d, axis, -1)
    except AxisError as e:
        raise AxisError(message) from e

    message = "`x` and `y` must have the same length along `axis`."
    if y is not None and x.shape[axis] != y.shape[axis]:
        raise ValueError(message)

    message = "`x` (and `y`, if provided) must be an array of real numbers."
    if not xp.isdtype(d.dtype, "real floating"):
        raise ValueError(message)

    zero_method = str(zero_method).lower()
    zero_methods = {"wilcox", "pratt", "zsplit"}
    message = f"`zero_method` must be one of {zero_methods}."
    if zero_method not in zero_methods:
        raise ValueError(message)

    corrections = {True, False}
    message = f"`correction` must be one of {corrections}."
    if correction not in corrections:
        raise ValueError(message)

    alternative = str(alternative).lower()
    alternatives = {"two-sided", "less", "greater"}
    message = f"`alternative` must be one of {alternatives}."
    if alternative not in alternatives:
        raise ValueError(message)

    if not isinstance(method, stats.PermutationMethod):
        methods = {"auto", "asymptotic", "exact"}
        message = (f"`method` must be one of {methods} or "
                   "an instance of `stats.PermutationMethod`.")
        if method not in methods:
            raise ValueError(message)
    output_z = True if method == 'asymptotic' else False

    if is_jax(xp) and str(method) in {"auto", "exact"}:
        message = ("When using `wilcoxon` with `jax.numpy` arrays, `method` must be "
                   "either 'asymptotic' or an instance of `stats.PermutationMethod`.")
        raise ValueError(message)

    if is_marray(xp) and (method != "asymptotic" or zero_method != 'zsplit'):
        message = ("Only `method='asymptotic'`/`zero_method='zsplit'` is compatible "
                   "with MArrays.")
        raise ValueError(message)

    # For small samples, we decide later whether to perform an exact test or a
    # permutation test. The reason is that the presence of ties is not
    # known at the input validation stage.
    n_zero = xp.count_nonzero(d == 0, axis=None)
    if method == "auto" and d.shape[-1] > 50:
        method = "asymptotic"

    return d, zero_method, correction, alternative, method, axis, output_z, n_zero, xp

