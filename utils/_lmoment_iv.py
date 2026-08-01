
def _lmoment_iv(sample, order, axis, sorted, standardize, xp):
    # input validation/standardization for `lmoment`
    sample = xp_promote(sample, force_floating=True, xp=xp)

    message = "`sample` must be an array of real numbers."
    if not xp.isdtype(sample.dtype, "real floating"):
        raise ValueError(message)

    message = "`order` must be a scalar or a non-empty array of positive integers."
    order = xp.arange(1, 5) if order is None else xp.asarray(order)
    if (not xp.isdtype(order.dtype, "integral") or order.size == 0 or order.ndim > 1
            or (not is_lazy_array(order) and xp.any(order <= 0))):
        raise ValueError(message)

    # input validation of non-array types can still be performed with NumPy
    axis = np.asarray(axis)[()]
    message = "`axis` must be an integer."
    if not np.issubdtype(axis.dtype, np.integer) or axis.ndim != 0:
        raise ValueError(message)
    axis = int(axis)

    sorted = np.asarray(sorted)[()]
    message = "`sorted` must be True or False."
    if not np.issubdtype(sorted.dtype, np.bool_) or sorted.ndim != 0:
        raise ValueError(message)
    sorted = bool(sorted)

    standardize = np.asarray(standardize)[()]
    message = "`standardize` must be True or False."
    if not np.issubdtype(standardize.dtype, np.bool_) or standardize.ndim != 0:
        raise ValueError(message)
    standardize = bool(standardize)

    sample = xp.moveaxis(sample, axis, -1)
    sample = xp.sort(sample, axis=-1) if not sorted else sample

    return sample, order, axis, sorted, standardize

