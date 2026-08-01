
def cumsum(
    input: Tensor,
    dim: int,
    *,
    dtype: DType | None = None,
    mask: Tensor | None = None,
) -> Tensor:
    if dtype is None:
        dtype = input.dtype
    dim_ = _canonical_dim(dim, input.ndim)[0]
    mask_input = _combine_input_and_mask(sum, input, mask)
    if mask_input.layout == torch.strided:
        return torch.cumsum(mask_input, dim_, dtype=dtype).to(dtype=dtype)
    else:
        raise ValueError(
            f"masked cumsum expects strided tensor (got {mask_input.layout} tensor)"
        )


def cumsum(x, axis=None, dtype=None):
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
        return (ops.add(a, b),)

    kwargs = _make_scan_inner(x, axis=axis, dtype=dtype)
    (result,) = ir.Scan.create(**kwargs, combine_fn=combine_fn)
    if result is None:
        return fallback_cumsum(x, dim=axis, dtype=dtype)
    return result


def cumsum(
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

    return a.cumsum(axis=axis, dtype=dtype)


def cumsum(
    a: TensorLikeType,
    dim: int,
    *,
    dtype: torch.dtype | None = None,
    out: Tensor | None = None,
) -> TensorLikeType:
    return _cumsumprod_common(func=sum, init=0, a=a, dim=dim, dtype=dtype, out=out)


def cumsum(g: jit_utils.GraphContext, self, dim, dtype=None):
    dim_tensor = g.op("Constant", value_t=torch.tensor(dim, dtype=torch.int))
    if dtype and dtype.node().kind() != "prim::Constant":
        parsed_dtype = symbolic_helper._get_const(dtype, "i", "dtype")
        cast = g.op(
            "Cast", self, to_i=_type_utils.JitScalarType(parsed_dtype).onnx_type()
        )
    else:
        cast = self
    csum = g.op("CumSum", cast, dim_tensor)
    return csum


def cumsum(g: jit_utils.GraphContext, input, dim, dtype) -> None:
    symbolic_helper._onnx_opset_unsupported("cumsum", 9, 11, input)


def cumsum(whatever):
    """
    This is the {method} method.

    It computes the cumulative {operation}.
    """


def cumsum(values: np.ndarray, *, skipna: bool = True) -> np.ndarray:
    return _cum_func(np.cumsum, values, skipna=skipna)


def cumsum(
    values: np.ndarray, mask: npt.NDArray[np.bool_], *, skipna: bool = True
) -> tuple[np.ndarray, npt.NDArray[np.bool_]]:
    return _cum_func(np.cumsum, values, mask, skipna=skipna)


def cumsum(a, axis=None, dtype=None, out=None):
    """
    Return the cumulative sum of the elements along a given axis.

    Parameters
    ----------
    a : array_like
        Input array.
    axis : int, optional
        Axis along which the cumulative sum is computed. The default
        (None) is to compute the cumsum over the flattened array.
    dtype : dtype, optional
        Type of the returned array and of the accumulator in which the
        elements are summed.  If `dtype` is not specified, it defaults
        to the dtype of `a`, unless `a` has an integer dtype with a
        precision less than that of the default platform integer.  In
        that case, the default platform integer is used.
    out : ndarray, optional
        Alternative output array in which to place the result. It must
        have the same shape and buffer length as the expected output
        but the type will be cast if necessary. See :ref:`ufuncs-output-type`
        for more details.

    Returns
    -------
    cumsum_along_axis : ndarray.
        A new array holding the result is returned unless `out` is
        specified, in which case a reference to `out` is returned. The
        result has the same size as `a`, and the same shape as `a` if
        `axis` is not None or `a` is a 1-d array.

    See Also
    --------
    cumulative_sum : Array API compatible alternative for ``cumsum``.
    sum : Sum array elements.
    trapezoid : Integration of array values using composite trapezoidal rule.
    diff : Calculate the n-th discrete difference along given axis.

    Notes
    -----
    Arithmetic is modular when using integer types, and no error is
    raised on overflow.

    ``cumsum(a)[-1]`` may not be equal to ``sum(a)`` for floating-point
    values since ``sum`` may use a pairwise summation routine, reducing
    the roundoff-error. See `sum` for more information.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1,2,3], [4,5,6]])
    >>> a
    array([[1, 2, 3],
           [4, 5, 6]])
    >>> np.cumsum(a)
    array([ 1,  3,  6, 10, 15, 21])
    >>> np.cumsum(a, dtype=np.float64)  # specifies type of output value(s)
    array([  1.,   3.,   6.,  10.,  15.,  21.])

    >>> np.cumsum(a,axis=0)      # sum over rows for each of the 3 columns
    array([[1, 2, 3],
           [5, 7, 9]])
    >>> np.cumsum(a,axis=1)      # sum over columns for each of the 2 rows
    array([[ 1,  3,  6],
           [ 4,  9, 15]])

    ``cumsum(b)[-1]`` may not be equal to ``sum(b)``

    >>> b = np.array([1, 2e-9, 3e-9] * 1000000)
    >>> b.cumsum()[-1]
    1000000.0050045159
    >>> b.sum()
    1000000.0050000029

    """
    return _wrapfunc(a, 'cumsum', axis=axis, dtype=dtype, out=out)


def cumsum(a: ArrayLike, axis: int | None = None,
           dtype: DTypeLike | None = None, out: None = None) -> Array:
  """Cumulative sum of elements along an axis.

  JAX implementation of :func:`numpy.cumsum`.

  Args:
    a: N-dimensional array to be accumulated.
    axis: integer axis along which to accumulate. If None (default), then
      array will be flattened and accumulated along the flattened axis.
    dtype: optionally specify the dtype of the output. If not specified,
      then the output dtype will match the input dtype.
    out: unused by JAX

  Returns:
    An array containing the accumulated sum along the given axis.

  See also:
    - :func:`jax.numpy.cumulative_sum`: cumulative sum via the array API standard.
    - :meth:`jax.numpy.add.accumulate`: cumulative sum via ufunc methods.
    - :func:`jax.numpy.nancumsum`: cumulative sum ignoring NaN values.
    - :func:`jax.numpy.sum`: sum along axis

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.cumsum(x)  # flattened cumulative sum
    Array([ 1,  3,  6, 10, 15, 21], dtype=int32)
    >>> jnp.cumsum(x, axis=1)  # cumulative sum along axis 1
    Array([[ 1,  3,  6],
           [ 4,  9, 15]], dtype=int32)
  """
  return _cumulative_reduction("cumsum", control_flow.cumsum, a, axis, dtype, out)


def cumsum(x: jax.Array, *, mask: jax.Array | None = None) -> jax.Array:
  """Returns the cumulative sum of the array along its innermost axis.

  This differs from `jnp.cumsum` in that it takes an additional `mask` argument.

  Args:
    x: An array of integers or floats.
    mask: An optional array of booleans, which specifies which elements of `x`
      are eligible for summing. If `None`, all elements are eligible.
  """
  if x.ndim != 1:
    raise NotImplementedError(f"cumsum: x={x.aval} must be rank 1")
  if mask is None:
    mask = lax.full(x.shape, True)
  return masked_cumsum_p.bind(x, mask)


def cumsum(operand: Array, axis: int = 0, reverse: bool = False) -> Array:
  """Computes a cumulative sum along `axis`."""
  return cumsum_p.bind(operand, axis=int(axis), reverse=bool(reverse))

