
def cumprod(
    input: Tensor,
    dim: int,
    *,
    dtype: DType | None = None,
    mask: Tensor | None = None,
) -> Tensor:
    if dtype is None:
        dtype = input.dtype
    dim_ = _canonical_dim(dim, input.ndim)[0]
    mask_input = _combine_input_and_mask(prod, input, mask)
    if mask_input.layout == torch.strided:
        return torch.cumprod(mask_input, dim_, dtype=dtype).to(dtype=dtype)
    else:
        raise ValueError(
            f"masked cumprod expects strided tensor (got {mask_input.layout} tensor)"
        )


def cumprod(x, axis=None, dtype=None):
    if (
        is_integer_dtype(x.get_dtype()) or is_boolean_dtype(x.get_dtype())
    ) and dtype is None:
        dtype = torch.int64

    if len(x.get_size()) == 0:
        assert axis in [0, -1]
        dtype = dtype or x.get_dtype()
        return to_dtype(x, dtype, copy=True)

    def combine_fn(a_tuple, b_tuple):
        (a,) = a_tuple
        (b,) = b_tuple
        return (ops.mul(a, b),)

    kwargs = _make_scan_inner(x, axis=axis, dtype=dtype)
    (result,) = ir.Scan.create(**kwargs, combine_fn=combine_fn)
    if result is None:
        return fallback_cumprod(x, dim=axis, dtype=dtype)
    return result


def cumprod(
    a: ArrayLike,
    axis: AxisLike = None,
    dtype: DTypeLike | None = None,
    out: OutArray | None = None,
):
    if dtype == torch.bool:
        dtype = _dtypes_impl.default_dtypes().int_dtype
    if dtype is None:
        dtype = a.dtype

    (a,), axis = _util.axis_none_flatten(a, axis=axis)
    axis = _util.normalize_axis_index(axis, a.ndim)

    return a.cumprod(axis=axis, dtype=dtype)


def cumprod(
    a: TensorLikeType,
    dim: int,
    *,
    dtype: torch.dtype | None = None,
    out: Tensor | None = None,
) -> TensorLikeType:
    return _cumsumprod_common(func=prod, init=1, a=a, dim=dim, dtype=dtype, out=out)


def cumprod(
    values: np.ndarray, mask: npt.NDArray[np.bool_], *, skipna: bool = True
) -> tuple[np.ndarray, npt.NDArray[np.bool_]]:
    return _cum_func(np.cumprod, values, mask, skipna=skipna)


def cumprod(a, axis=None, dtype=None, out=None):
    """
    Return the cumulative product of elements along a given axis.

    Parameters
    ----------
    a : array_like
        Input array.
    axis : int, optional
        Axis along which the cumulative product is computed.  By default
        the input is flattened.
    dtype : dtype, optional
        Type of the returned array, as well as of the accumulator in which
        the elements are multiplied.  If *dtype* is not specified, it
        defaults to the dtype of `a`, unless `a` has an integer dtype with
        a precision less than that of the default platform integer.  In
        that case, the default platform integer is used instead.
    out : ndarray, optional
        Alternative output array in which to place the result. It must
        have the same shape and buffer length as the expected output
        but the type of the resulting values will be cast if necessary.

    Returns
    -------
    cumprod : ndarray
        A new array holding the result is returned unless `out` is
        specified, in which case a reference to out is returned.

    See Also
    --------
    cumulative_prod : Array API compatible alternative for ``cumprod``.
    :ref:`ufuncs-output-type`

    Notes
    -----
    Arithmetic is modular when using integer types, and no error is
    raised on overflow.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([1,2,3])
    >>> np.cumprod(a) # intermediate results 1, 1*2
    ...               # total product 1*2*3 = 6
    array([1, 2, 6])
    >>> a = np.array([[1, 2, 3], [4, 5, 6]])
    >>> np.cumprod(a, dtype=np.float64)  # specify type of output
    array([   1.,    2.,    6.,   24.,  120.,  720.])

    The cumulative product for each column (i.e., over the rows) of `a`:

    >>> np.cumprod(a, axis=0)
    array([[ 1,  2,  3],
           [ 4, 10, 18]])

    The cumulative product for each row (i.e. over the columns) of `a`:

    >>> np.cumprod(a,axis=1)
    array([[  1,   2,   6],
           [  4,  20, 120]])

    """
    return _wrapfunc(a, 'cumprod', axis=axis, dtype=dtype, out=out)


def cumprod(a: ArrayLike, axis: int | None = None,
            dtype: DTypeLike | None = None, out: None = None) -> Array:
  """Cumulative product of elements along an axis.

  JAX implementation of :func:`numpy.cumprod`.

  Args:
    a: N-dimensional array to be accumulated.
    axis: integer axis along which to accumulate. If None (default), then
      array will be flattened and accumulated along the flattened axis.
    dtype: optionally specify the dtype of the output. If not specified,
      then the output dtype will match the input dtype.
    out: unused by JAX

  Returns:
    An array containing the accumulated product along the given axis.

  See also:
    - :meth:`jax.numpy.multiply.accumulate`: cumulative product via ufunc methods.
    - :func:`jax.numpy.nancumprod`: cumulative product ignoring NaN values.
    - :func:`jax.numpy.prod`: product along axis

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.cumprod(x)  # flattened cumulative product
    Array([  1,   2,   6,  24, 120, 720], dtype=int32)
    >>> jnp.cumprod(x, axis=1)  # cumulative product along axis 1
    Array([[  1,   2,   6],
           [  4,  20, 120]], dtype=int32)
  """
  return _cumulative_reduction("cumprod", control_flow.cumprod, a, axis, dtype, out)


def cumprod(operand: Array, axis: int = 0, reverse: bool = False) -> Array:
  """Computes a cumulative product along `axis`."""
  return cumprod_p.bind(operand, axis=int(axis), reverse=bool(reverse))

