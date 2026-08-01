
def xp_promote(*args, broadcast=False, force_floating=False, xp):
    """
    Promotes elements of *args to result dtype, ignoring `None`s.
    Includes options for forcing promotion to floating point and
    broadcasting the arrays, again ignoring `None`s.
    Type promotion rules follow `xp_result_type` instead of `xp.result_type`.

    Typically, this function will be called shortly after `array_namespace`
    on a subset of the arguments passed to `array_namespace`.

    This function accepts array-like iterables, which are immediately converted
    to the namespace's arrays before result type calculation. Consequently, the
    result dtype may be different when an argument is `1.` vs `[1.]`.

    See Also
    --------
    xp_result_type
    """
    if not args:
        return args

    # prevent double conversion of iterable to array
    # avoid `np.iterable` for torch arrays due to pytorch/pytorch#143334
    # don't use `array_api_compat.is_array_api_obj` as it returns True for NumPy scalars
    args = [(_asarray(arg, subok=True, xp=xp) if is_torch_array(arg) or np.iterable(arg)
            else arg) for arg in args]

    dtype = xp_result_type(*args, force_floating=force_floating, xp=xp)

    args = [(_asarray(arg, dtype=dtype, subok=True, xp=xp) if arg is not None else arg)
            for arg in args]

    if not broadcast:
        return args[0] if len(args)==1 else tuple(args)

    args_not_none = [arg for arg in args if arg is not None]

    # determine result shape
    shapes = {arg.shape for arg in args_not_none}
    try:
        shape = (np.broadcast_shapes(*shapes) if len(shapes) != 1
                 else args_not_none[0].shape)
    except ValueError as e:
        message = "Array shapes are incompatible for broadcasting."
        raise ValueError(message) from e

    out = []
    for arg in args:
        if arg is None:
            out.append(arg)
            continue

        # broadcast only if needed
        # Even if two arguments need broadcasting, this is faster than
        # `broadcast_arrays`, especially since we've already determined `shape`
        if arg.shape != shape:
            kwargs = {'subok': True} if is_numpy(xp) else {}
            arg = xp.broadcast_to(arg, shape, **kwargs)

        # This is much faster than xp.astype(arg, dtype, copy=False)
        if arg.dtype != dtype:
            arg = xp.astype(arg, dtype)

        out.append(arg)

    return out[0] if len(out)==1 else tuple(out)

