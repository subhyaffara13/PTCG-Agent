
def create_diagonal(
    x: Array, /, *, offset: int = 0, xp: ModuleType | None = None
) -> Array:
    """
    Construct a diagonal array.

    Parameters
    ----------
    x : array
        An array having shape ``(*batch_dims, k)``.
    offset : int, optional
        Offset from the leading diagonal (default is ``0``).
        Use positive ints for diagonals above the leading diagonal,
        and negative ints for diagonals below the leading diagonal.
    xp : array_namespace, optional
        The standard-compatible namespace for `x`. Default: infer.

    Returns
    -------
    array
        An array having shape ``(*batch_dims, k+abs(offset), k+abs(offset))`` with `x`
        on the diagonal (offset by `offset`).

    Examples
    --------
    >>> import array_api_strict as xp
    >>> import array_api_extra as xpx
    >>> x = xp.asarray([2, 4, 8])

    >>> xpx.create_diagonal(x, xp=xp)
    Array([[2, 0, 0],
           [0, 4, 0],
           [0, 0, 8]], dtype=array_api_strict.int64)

    >>> xpx.create_diagonal(x, offset=-2, xp=xp)
    Array([[0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [2, 0, 0, 0, 0],
           [0, 4, 0, 0, 0],
           [0, 0, 8, 0, 0]], dtype=array_api_strict.int64)
    """
    if xp is None:
        xp = array_namespace(x)

    if x.ndim == 0:
        err_msg = "`x` must be at least 1-dimensional."
        raise ValueError(err_msg)

    if is_torch_namespace(xp):
        return xp.diag_embed(x, offset=offset, dim1=-2, dim2=-1)

    if (
        is_dask_namespace(xp)
        or is_cupy_namespace(xp)
        or is_numpy_namespace(xp)
        or is_jax_namespace(xp)
    ) and (x.ndim < 2):
        return xp.diag(x, k=offset)

    return _funcs.create_diagonal(x, offset=offset, xp=xp)


def create_diagonal(
    x: Array, /, *, offset: int = 0, xp: ModuleType
) -> Array:  # numpydoc ignore=PR01,RT01
    """See docstring in array_api_extra._delegation."""
    x_shape = eager_shape(x)
    batch_dims = x_shape[:-1]
    n = x_shape[-1] + abs(offset)
    diag = xp.zeros((*batch_dims, n**2), dtype=x.dtype, device=_compat.device(x))

    target_slice = slice(
        offset if offset >= 0 else abs(offset) * n,
        min(n * (n - offset), diag.shape[-1]),
        n + 1,
    )
    for index in ndindex(*batch_dims):
        diag = at(diag)[(*index, target_slice)].set(x[(*index, slice(None))])
    return xp.reshape(diag, (*batch_dims, n, n))

