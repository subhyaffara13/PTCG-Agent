
def atleast_nd(x: Array, /, *, ndim: int, xp: ModuleType | None = None) -> Array:
    """
    Recursively expand the dimension of an array to at least `ndim`.

    Parameters
    ----------
    x : array
        Input array.
    ndim : int
        The minimum number of dimensions for the result.
    xp : array_namespace, optional
        The standard-compatible namespace for `x`. Default: infer.

    Returns
    -------
    array
        An array with ``res.ndim`` >= `ndim`.
        If ``x.ndim`` >= `ndim`, `x` is returned.
        If ``x.ndim`` < `ndim`, `x` is expanded by prepending new axes
        until ``res.ndim`` equals `ndim`.

    Examples
    --------
    >>> import array_api_strict as xp
    >>> import array_api_extra as xpx
    >>> x = xp.asarray([1])
    >>> xpx.atleast_nd(x, ndim=3, xp=xp)
    Array([[[1]]], dtype=array_api_strict.int64)

    >>> x = xp.asarray([[[1, 2],
    ...                  [3, 4]]])
    >>> xpx.atleast_nd(x, ndim=1, xp=xp) is x
    True
    """
    if xp is None:
        xp = array_namespace(x)

    if 1 <= ndim <= 2 and (
        is_numpy_namespace(xp)
        or is_jax_namespace(xp)
        or is_dask_namespace(xp)
        or is_cupy_namespace(xp)
        or is_torch_namespace(xp)
    ):
        return getattr(xp, f"atleast_{ndim}d")(x)

    return _funcs.atleast_nd(x, ndim=ndim, xp=xp)


def atleast_nd(x: Array, /, *, ndim: int, xp: ModuleType) -> Array:
    # numpydoc ignore=PR01,RT01
    """See docstring in array_api_extra._delegation."""

    if x.ndim < ndim:
        x = xp.expand_dims(x, axis=0)
        x = atleast_nd(x, ndim=ndim, xp=xp)
    return x

