from typing import Callable

def apply_where(  # numpydoc ignore=GL08
    cond: Array,
    args: Array | tuple[Array, ...],
    f1: Callable[..., Array],
    f2: Callable[..., Array],
    /,
    *,
    kwargs: dict[str, Array] | None = None,
    xp: ModuleType | None = None,
) -> Array: ...


def apply_where(  # numpydoc ignore=GL08
    cond: Array,
    args: Array | tuple[Array, ...],
    f1: Callable[..., Array],
    /,
    *,
    fill_value: Array | complex,
    kwargs: dict[str, Array] | None = None,
    xp: ModuleType | None = None,
) -> Array: ...


def apply_where(  # numpydoc ignore=PR01,PR02
    cond: Array,
    args: Array | tuple[Array, ...],
    f1: Callable[..., Array],
    f2: Callable[..., Array] | None = None,
    /,
    *,
    fill_value: Array | complex | None = None,
    kwargs: dict[str, Array] | None = None,
    xp: ModuleType | None = None,
) -> Array:
    """
    Run one of two elementwise functions depending on a condition.

    Equivalent to ``f1(*args) if cond else fill_value`` performed elementwise
    when `fill_value` is defined, otherwise to ``f1(*args) if cond else f2(*args)``.

    Parameters
    ----------
    cond : array
        The condition, expressed as a boolean array.
    args : Array or tuple of Arrays
        Argument(s) to `f1` (and `f2`). Must be broadcastable with `cond`.
    f1 : callable
        Elementwise function of `args`, returning a single array.
        Where `cond` is True, output will be ``f1(arg0[cond], arg1[cond], ...)``.
    f2 : callable, optional
        Elementwise function of `args`, returning a single array.
        Where `cond` is False, output will be ``f2(arg0[cond], arg1[cond], ...)``.
        Mutually exclusive with `fill_value`.
    fill_value : Array or scalar, optional
        If provided, value with which to fill output array where `cond` is False.
        It does not need to be scalar; it needs however to be broadcastable with
        `cond` and `args`.
        Mutually exclusive with `f2`. You must provide one or the other.
    kwargs : dict of str : Array pairs
        Keyword argument(s) to `f1` (and `f2`). Values must be broadcastable with
        `cond`.
    xp : array_namespace, optional
        The standard-compatible namespace for `cond` and `args`. Default: infer.

    Returns
    -------
    Array
        An array with elements from the output of `f1` where `cond` is True and either
        the output of `f2` or `fill_value` where `cond` is False. The returned array has
        data type determined by type promotion rules between the output of `f1` and
        either `fill_value` or the output of `f2`.

    Notes
    -----
    ``xp.where(cond, f1(*args), f2(*args))`` requires explicitly evaluating `f1` even
    when `cond` is False, and `f2` when cond is True. This function evaluates each
    function only for their matching condition, if the backend allows for it.

    On Dask, `f1` and `f2` are applied to the individual chunks and should use functions
    from the namespace of the chunks.

    Examples
    --------
    >>> import array_api_strict as xp
    >>> import array_api_extra as xpx
    >>> a = xp.asarray([5, 4, 3])
    >>> b = xp.asarray([0, 2, 2])
    >>> def f(a, b):
    ...     return a // b
    >>> xpx.apply_where(b != 0, (a, b), f, fill_value=xp.nan)
    array([ nan,  2., 1.])
    """
    # Parse and normalize arguments
    if (f2 is None) == (fill_value is None):
        msg = "Exactly one of `fill_value` or `f2` must be given."
        raise TypeError(msg)
    args_ = list(args) if isinstance(args, tuple) else [args]
    del args

    kwargs_ = {} if kwargs is None else kwargs
    kwkeys = list(kwargs_.keys())
    args_ = [*args_, *kwargs_.values()]
    del kwargs

    xp = array_namespace(cond, fill_value, *args_) if xp is None else xp

    if isinstance(fill_value, int | float | complex | NoneType):
        cond, *args_ = xp.broadcast_arrays(cond, *args_)
    else:
        cond, fill_value, *args_ = xp.broadcast_arrays(cond, fill_value, *args_)

    if is_dask_namespace(xp):
        meta_xp = meta_namespace(cond, fill_value, *args_, xp=xp)
        # map_blocks doesn't descend into tuples of Arrays
        return xp.map_blocks(
            _apply_where, cond, f1, f2, fill_value, *args_, kwkeys=kwkeys, xp=meta_xp
        )

    return _apply_where(cond, f1, f2, fill_value, *args_, kwkeys=kwkeys, xp=xp)

