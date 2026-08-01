
def cumulative_prod(
    x: Array,
    /,
    xp: Namespace,
    *,
    axis: int | None = None,
    dtype: DType | None = None,
    include_initial: bool = False,
    **kwargs: object,
) -> Array:
    wrapped_xp = array_namespace(x)

    if axis is None:
        if x.ndim > 1:
            raise ValueError(
                "axis must be specified in cumulative_prod for more than one dimension"
            )
        axis = 0

    res = xp.cumprod(x, axis=axis, dtype=dtype, **kwargs)

    # np.cumprod does not support include_initial
    if include_initial:
        initial_shape = list(x.shape)
        initial_shape[axis] = 1
        res = xp.concatenate(
            [
                wrapped_xp.ones(
                    shape=initial_shape, dtype=res.dtype, device=_get_device(res)
                ),
                res,
            ],
            axis=axis,
        )
    return res


def cumulative_prod(x, /, *, axis=None, dtype=None, out=None,
                    include_initial=False):
    """
    Return the cumulative product of elements along a given axis.

    This function is an Array API compatible alternative to `numpy.cumprod`.

    Parameters
    ----------
    x : array_like
        Input array.
    axis : int, optional
        Axis along which the cumulative product is computed. The default
        (None) is only allowed for one-dimensional arrays. For arrays
        with more than one dimension ``axis`` is required.
    dtype : dtype, optional
        Type of the returned array, as well as of the accumulator in which
        the elements are multiplied.  If ``dtype`` is not specified, it
        defaults to the dtype of ``x``, unless ``x`` has an integer dtype
        with a precision less than that of the default platform integer.
        In that case, the default platform integer is used instead.
    out : ndarray, optional
        Alternative output array in which to place the result. It must
        have the same shape and buffer length as the expected output
        but the type of the resulting values will be cast if necessary.
        See :ref:`ufuncs-output-type` for more details.
    include_initial : bool, optional
        Boolean indicating whether to include the initial value (ones) as
        the first value in the output. With ``include_initial=True``
        the shape of the output is different than the shape of the input.
        Default: ``False``.

    Returns
    -------
    cumulative_prod_along_axis : ndarray
        A new array holding the result is returned unless ``out`` is
        specified, in which case a reference to ``out`` is returned. The
        result has the same shape as ``x`` if ``include_initial=False``.

    Notes
    -----
    Arithmetic is modular when using integer types, and no error is
    raised on overflow.

    Examples
    --------
    >>> a = np.array([1, 2, 3])
    >>> np.cumulative_prod(a)  # intermediate results 1, 1*2
    ...                        # total product 1*2*3 = 6
    array([1, 2, 6])
    >>> a = np.array([1, 2, 3, 4, 5, 6])
    >>> np.cumulative_prod(a, dtype=np.float64)  # specify type of output
    array([   1.,    2.,    6.,   24.,  120.,  720.])

    The cumulative product for each column (i.e., over the rows) of ``b``:

    >>> b = np.array([[1, 2, 3], [4, 5, 6]])
    >>> np.cumulative_prod(b, axis=0)
    array([[ 1,  2,  3],
           [ 4, 10, 18]])

    The cumulative product for each row (i.e. over the columns) of ``b``:

    >>> np.cumulative_prod(b, axis=1)
    array([[  1,   2,   6],
           [  4,  20, 120]])

    """
    return _cumulative_func(x, um.multiply, axis, dtype, out, include_initial)


def cumulative_prod(
    x: ArrayLike, /, *, axis: int | None = None,
    dtype: DTypeLike | None = None,
    include_initial: bool = False) -> Array:
  """Cumulative product along the axis of an array.

  JAX implementation of :func:`numpy.cumulative_prod`.

  Args:
    x: N-dimensional array
    axis: integer axis along which to accumulate. If ``x`` is one-dimensional,
      this argument is optional and defaults to zero.
    dtype: optional dtype of the output.
    include_initial: if True, then include the initial value in the cumulative
      product. Default is False.

  Returns:
    An array containing the accumulated values.

  See Also:
    - :func:`jax.numpy.cumprod`: alternative API for cumulative product.
    - :func:`jax.numpy.nancumprod`: cumulative product while ignoring NaN values.
    - :func:`jax.numpy.multiply.accumulate`: cumulative product via the ufunc API.

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.cumulative_prod(x, axis=1)
    Array([[  1,   2,   6],
           [  4,  20, 120]], dtype=int32)
    >>> jnp.cumulative_prod(x, axis=1, include_initial=True)
    Array([[  1,   1,   2,   6],
           [  1,   4,  20, 120]], dtype=int32)
  """
  x = ensure_arraylike("cumulative_prod", x)
  if x.ndim == 0:
    raise ValueError(
      "The input must be non-scalar to take a cumulative product, however a "
      "scalar value or scalar array was given."
    )
  if axis is None:
    axis = 0
    if x.ndim > 1:
      raise ValueError(
        f"The input array has rank {x.ndim}, however axis was not set to an "
        "explicit value. The axis argument is only optional for one-dimensional "
        "arrays.")

  axis = canonicalize_axis(axis, x.ndim)
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype)
  out = _cumulative_reduction("cumulative_prod", control_flow.cumprod, x, axis, dtype)
  if include_initial:
    zeros_shape = list(x.shape)
    zeros_shape[axis] = 1
    out = lax.concatenate(
      [lax.full(zeros_shape, 1, dtype=out.dtype), out],
      dimension=axis)
  return out

