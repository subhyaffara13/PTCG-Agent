
def _masked_apply(f, *, args, kwargs=None, xp):
    # Unmask array arguments, evaluate function, and apply result mask to outputs.
    # Assumes that when `xp` is an MArray namespace, there is at least one MArray
    # in `args`/`kwargs` and MArrays are the only objects in `args`/`kwargs` with
    # `data` and `mask` attributes. Could/should combine with `xpx.lazy_apply`.
    kwargs = {} if kwargs is None else kwargs

    if not is_marray(xp):
        return f(*args, **kwargs)

    arg_data = (getattr(arg, 'data', arg) for arg in args)
    kwarg_data = (getattr(val, 'data', val) for val in kwargs.values())
    res = f(*arg_data, **dict(zip(kwarg_data, kwargs.keys())))

    masks = (arr.mask for arr in (*args, *kwargs.values()) if hasattr(arr, 'mask'))
    mask = functools.reduce(operator.or_, masks)
    return ((xp.asarray(out, mask=mask) for out in res) if isinstance(res, tuple)
            else xp.asarray(res, mask=mask))

