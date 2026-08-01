
def cumulative_sum(
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

    # TODO: The standard is not clear about what should happen when x.ndim == 0.
    if axis is None:
        if x.ndim > 1:
            raise ValueError(
                "axis must be specified in cumulative_sum for more than one dimension"
            )
        axis = 0

    res = xp.cumsum(x, axis=axis, dtype=dtype, **kwargs)

    # np.cumsum does not support include_initial
    if include_initial:
        initial_shape = list(x.shape)
        initial_shape[axis] = 1
        res = xp.concatenate(
            [
                wrapped_xp.zeros(
                    shape=initial_shape, dtype=res.dtype, device=_get_device(res)
                ),
                res,
            ],
            axis=axis,
        )
    return res


def cumulative_sum(x, /, *, axis=None, dtype=None, out=None,
                   include_initial=False):
    """
    Return the cumulative sum of the elements along a given axis.

    This function is an Array API compatible alternative to `numpy.cumsum`.

    Parameters
    ----------
    x : array_like
        Input array.
    axis : int, optional
        Axis along which the cumulative sum is computed. The default
        (None) is only allowed for one-dimensional arrays. For arrays
        with more than one dimension ``axis`` is required.
    dtype : dtype, optional
        Type of the returned array and of the accumulator in which the
        elements are summed.  If ``dtype`` is not specified, it defaults
        to the dtype of ``x``, unless ``x`` has an integer dtype with
        a precision less than that of the default platform integer.
        In that case, the default platform integer is used.
    out : ndarray, optional
        Alternative output array in which to place the result. It must
        have the same shape and buffer length as the expected output
        but the type will be cast if necessary. See :ref:`ufuncs-output-type`
        for more details.
    include_initial : bool, optional
        Boolean indicating whether to include the initial value (zeros) as
        the first value in the output. With ``include_initial=True``
        the shape of the output is different than the shape of the input.
        Default: ``False``.

    Returns
    -------
    cumulative_sum_along_axis : ndarray
        A new array holding the result is returned unless ``out`` is
        specified, in which case a reference to ``out`` is returned. The
        result has the same shape as ``x`` if ``include_initial=False``.

    See Also
    --------
    sum : Sum array elements.
    trapezoid : Integration of array values using composite trapezoidal rule.
    diff : Calculate the n-th discrete difference along given axis.

    Notes
    -----
    Arithmetic is modular when using integer types, and no error is
    raised on overflow.

    ``cumulative_sum(a)[-1]`` may not be equal to ``sum(a)`` for
    floating-point values since ``sum`` may use a pairwise summation routine,
    reducing the roundoff-error. See `sum` for more information.

    Examples
    --------
    >>> a = np.array([1, 2, 3, 4, 5, 6])
    >>> a
    array([1, 2, 3, 4, 5, 6])
    >>> np.cumulative_sum(a)
    array([ 1,  3,  6, 10, 15, 21])
    >>> np.cumulative_sum(a, dtype=np.float64)  # specifies type of output value(s)
    array([  1.,   3.,   6.,  10.,  15.,  21.])

    >>> b = np.array([[1, 2, 3], [4, 5, 6]])
    >>> np.cumulative_sum(b,axis=0)  # sum over rows for each of the 3 columns
    array([[1, 2, 3],
           [5, 7, 9]])
    >>> np.cumulative_sum(b,axis=1)  # sum over columns for each of the 2 rows
    array([[ 1,  3,  6],
           [ 4,  9, 15]])

    ``cumulative_sum(c)[-1]`` may not be equal to ``sum(c)``

    >>> c = np.array([1, 2e-9, 3e-9] * 1000000)
    >>> np.cumulative_sum(c)[-1]
    1000000.0050045159
    >>> c.sum()
    1000000.0050000029

    """
    return _cumulative_func(x, um.add, axis, dtype, out, include_initial)


def cumulative_sum(
    x: ArrayLike, /, *, axis: int | None = None,
    dtype: DTypeLike | None = None,
    include_initial: bool = False) -> Array:
  """Cumulative sum along the axis of an array.

  JAX implementation of :func:`numpy.cumulative_sum`.

  Args:
    x: N-dimensional array
    axis: integer axis along which to accumulate. If ``x`` is one-dimensional,
      this argument is optional and defaults to zero.
    dtype: optional dtype of the output.
    include_initial: if True, then include the initial value in the cumulative
      sum. Default is False.

  Returns:
    An array containing the accumulated values.

  See Also:
    - :func:`jax.numpy.cumsum`: alternative API for cumulative sum.
    - :func:`jax.numpy.nancumsum`: cumulative sum while ignoring NaN values.
    - :func:`jax.numpy.add.accumulate`: cumulative sum via the ufunc API.

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.cumulative_sum(x, axis=1)
    Array([[ 1,  3,  6],
           [ 4,  9, 15]], dtype=int32)
    >>> jnp.cumulative_sum(x, axis=1, include_initial=True)
    Array([[ 0,  1,  3,  6],
           [ 0,  4,  9, 15]], dtype=int32)
  """
  x = ensure_arraylike("cumulative_sum", x)
  if x.ndim == 0:
    raise ValueError(
      "The input must be non-scalar to take a cumulative sum, however a "
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
  out = _cumsum_with_promotion(x, axis=axis, dtype=dtype)
  if include_initial:
    zeros_shape = list(x.shape)
    zeros_shape[axis] = 1
    out = lax.concatenate(
      [lax.full(zeros_shape, 0, dtype=out.dtype), out],
      dimension=axis)
  return out

