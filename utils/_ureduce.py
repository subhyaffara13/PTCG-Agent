
def _ureduce(a, func, keepdims=False, **kwargs):
    """
    Internal Function.
    Call `func` with `a` as first argument swapping the axes to use extended
    axis on functions that don't support it natively.

    Returns result and a.shape with axis dims set to 1.

    Parameters
    ----------
    a : array_like
        Input array or object that can be converted to an array.
    func : callable
        Reduction function capable of receiving a single axis argument.
        It is called with `a` as first argument followed by `kwargs`.
    kwargs : keyword arguments
        additional keyword arguments to pass to `func`.

    Returns
    -------
    result : tuple
        Result of func(a, **kwargs) and a.shape with axis dims set to 1
        which can be used to reshape the result to the same shape a ufunc with
        keepdims=True would produce.

    """
    a = np.asanyarray(a)
    axis = kwargs.get('axis')
    out = kwargs.get('out')

    if keepdims is np._NoValue:
        keepdims = False

    nd = a.ndim
    if axis is not None:
        axis = _nx.normalize_axis_tuple(axis, nd)

        if keepdims and out is not None:
            index_out = tuple(
                0 if i in axis else slice(None) for i in range(nd))
            kwargs['out'] = out[(Ellipsis, ) + index_out]

        if len(axis) == 1:
            kwargs['axis'] = axis[0]
        else:
            keep = sorted(set(range(nd)) - set(axis))
            nkeep = len(keep)

            def reshape_arr(a):
                # move axis that should not be reduced to front
                a = np.moveaxis(a, keep, range(nkeep))
                # merge reduced axis
                return a.reshape(a.shape[:nkeep] + (-1,))

            a = reshape_arr(a)

            weights = kwargs.get("weights")
            if weights is not None:
                kwargs["weights"] = reshape_arr(weights)

            kwargs['axis'] = -1
    elif keepdims and out is not None:
        index_out = (0, ) * nd
        kwargs['out'] = out[(Ellipsis, ) + index_out]

    r = func(a, **kwargs)

    if out is not None:
        return out

    if keepdims:
        if axis is None:
            index_r = (np.newaxis, ) * nd
        else:
            index_r = tuple(
                np.newaxis if i in axis else slice(None)
                for i in range(nd))
        r = r[(Ellipsis, ) + index_r]

    return r

