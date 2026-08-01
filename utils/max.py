
def max(g: jit_utils.GraphContext, self, dim_or_y=None, keepdim=None):
    return symbolic_helper._max_helper(g, self, dim_or_y, keepdim)


def max(g: jit_utils.GraphContext, self, dim_or_y=None, keepdim=None):
    # torch.max(input, other)
    if keepdim is None and dim_or_y is not None:
        warnings.warn(
            "Multidirectional broadcasting is not supported in opset 7. "
            "This might cause the onnx model to be incorrect, if inputs to max operators "
            "have different shapes",
            stacklevel=2,
        )
    return opset9.max(g, self, dim_or_y, keepdim)


def max(g: jit_utils.GraphContext, self, dim_or_y=None, keepdim=None):
    return symbolic_helper._max_helper(g, self, dim_or_y, keepdim)


def max(x: Array, /, *, axis: int | tuple[int, ...] | None = None, keepdims: bool = False) -> Array:
    # https://github.com/pytorch/pytorch/issues/29137
    if axis == ():
        return torch.clone(x)
    return torch.amax(x, axis, keepdims=keepdims)


def max(
    values: np.ndarray,
    mask: npt.NDArray[np.bool_],
    *,
    skipna: bool = True,
    axis: AxisInt | None = None,
):
    return _minmax(np.max, values=values, mask=mask, skipna=skipna, axis=axis)


def max(obj, axis=None, out=None, fill_value=None, keepdims=np._NoValue):
    kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}

    try:
        return obj.max(axis=axis, fill_value=fill_value, out=out, **kwargs)
    except (AttributeError, TypeError):
        # If obj doesn't have a max method, or if the method doesn't accept a
        # fill_value argument
        return asanyarray(obj).max(axis=axis, fill_value=fill_value,
                                   out=out, **kwargs)


def max(a, axis=None, out=None, keepdims=np._NoValue, initial=np._NoValue,
         where=np._NoValue):
    """
    Return the maximum of an array or maximum along an axis.

    Parameters
    ----------
    a : array_like
        Input data.
    axis : None or int or tuple of ints, optional
        Axis or axes along which to operate.  By default, flattened input is
        used. If this is a tuple of ints, the maximum is selected over
        multiple axes, instead of a single axis or all the axes as before.

    out : ndarray, optional
        Alternative output array in which to place the result.  Must
        be of the same shape and buffer length as the expected output.
        See :ref:`ufuncs-output-type` for more details.

    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the input array.

        If the default value is passed, then `keepdims` will not be
        passed through to the ``max`` method of sub-classes of
        `ndarray`, however any non-default value will be.  If the
        sub-class' method does not implement `keepdims` any
        exceptions will be raised.

    initial : scalar, optional
        The minimum value of an output element. Must be present to allow
        computation on empty slice. See `~numpy.ufunc.reduce` for details.

    where : array_like of bool, optional
        Elements to compare for the maximum. See `~numpy.ufunc.reduce`
        for details.

    Returns
    -------
    max : ndarray or scalar
        Maximum of `a`. If `axis` is None, the result is a scalar value.
        If `axis` is an int, the result is an array of dimension
        ``a.ndim - 1``. If `axis` is a tuple, the result is an array of
        dimension ``a.ndim - len(axis)``.

    See Also
    --------
    min :
        The minimum value of an array along a given axis, propagating any NaNs.
    nanmax :
        The maximum value of an array along a given axis, ignoring any NaNs.
    maximum :
        Element-wise maximum of two arrays, propagating any NaNs.
    fmax :
        Element-wise maximum of two arrays, ignoring any NaNs.
    argmax :
        Return the indices of the maximum values.

    nanmin, minimum, fmin

    Notes
    -----
    NaN values are propagated, that is if at least one item is NaN, the
    corresponding max value will be NaN as well. To ignore NaN values
    (MATLAB behavior), please use nanmax.

    Don't use `~numpy.max` for element-wise comparison of 2 arrays; when
    ``a.shape[0]`` is 2, ``maximum(a[0], a[1])`` is faster than
    ``max(a, axis=0)``.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.arange(4).reshape((2,2))
    >>> a
    array([[0, 1],
           [2, 3]])
    >>> np.max(a)           # Maximum of the flattened array
    3
    >>> np.max(a, axis=0)   # Maxima along the first axis
    array([2, 3])
    >>> np.max(a, axis=1)   # Maxima along the second axis
    array([1, 3])
    >>> np.max(a, where=[False, True], initial=-1, axis=0)
    array([-1,  3])
    >>> b = np.arange(5, dtype=np.float64)
    >>> b[2] = np.nan
    >>> np.max(b)
    np.float64(nan)
    >>> np.max(b, where=~np.isnan(b), initial=-1)
    4.0
    >>> np.nanmax(b)
    4.0

    You can use an initial value to compute the maximum of an empty slice, or
    to initialize it to a different value:

    >>> np.max([[-50], [10]], axis=-1, initial=0)
    array([ 0, 10])

    Notice that the initial value is used as one of the elements for which the
    maximum is determined, unlike for the default argument Python's max
    function, which is only used for empty iterables.

    >>> np.max([5], initial=6)
    6
    >>> max([5], default=6)
    5
    """
    return _wrapreduction(a, np.maximum, 'max', axis, None, out,
                          keepdims=keepdims, initial=initial, where=where)


def MAX(x, y):
    if mpf_ge(x, y):
        return x
    return y


def max(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise maximum: :math:`\mathrm{max}(x, y)`.

  This function lowers directly to the `stablehlo.maximum`_ operation for
  non-complex inputs. For complex numbers, this uses a lexicographic
  comparison on the `(real, imaginary)` pairs.

  Args:
    x, y: Input arrays. Must have matching dtypes. If neither is a scalar,
      ``x`` and ``y`` must have the same rank and be broadcast compatible.

  Returns:
    An array of the same dtype as ``x`` and ``y`` containing the elementwise
    maximum.

  See also:
    - :func:`jax.numpy.maximum`: more flexibly NumPy-style maximum.
    - :func:`jax.lax.reduce_max`: maximum along an axis of an array.
    - :func:`jax.lax.min`: elementwise minimum.

  .. _stablehlo.maximum: https://openxla.org/stablehlo/spec#maximum
  """
  x, y = core.auto_insert_reshard(x, y)
  return max_p.bind(x, y)


def max(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False, initial: ArrayLike | None = None,
        where: ArrayLike | None = None) -> Array:
  r"""Return the maximum of the array elements along a given axis.

  JAX implementation of :func:`numpy.max`.

  Args:
    a: Input array.
    axis: int or array, default=None. Axis along which the maximum to be computed.
      If None, the maximum is computed along all the axes.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    initial: int or array, default=None. Initial value for the maximum.
    where: int or array of boolean dtype, default=None. The elements to be used
      in the maximum. Array should be broadcast compatible to the input.
      ``initial`` must be specified when ``where`` is used.
    out: Unused by JAX.

  Returns:
    An array of maximum values along the given axis.

  See also:
    - :func:`jax.numpy.min`: Compute the minimum of array elements along a given
      axis.
    - :func:`jax.numpy.sum`: Compute the sum of array elements along a given axis.
    - :func:`jax.numpy.prod`: Compute the product of array elements along a given
      axis.

  Examples:

    By default, ``jnp.max`` computes the maximum of elements along all the axes.

    >>> x = jnp.array([[9, 3, 4, 5],
    ...                [5, 2, 7, 4],
    ...                [8, 1, 3, 6]])
    >>> jnp.max(x)
    Array(9, dtype=int32)

    If ``axis=1``, the maximum will be computed along axis 1.

    >>> jnp.max(x, axis=1)
    Array([9, 7, 8], dtype=int32)

    If ``keepdims=True``, ``ndim`` of the output will be same of that of the input.

    >>> jnp.max(x, axis=1, keepdims=True)
    Array([[9],
           [7],
           [8]], dtype=int32)

    To include only specific elements in computing the maximum, you can use
    ``where``. It can either have same dimension as input

    >>> where=jnp.array([[0, 0, 1, 0],
    ...                  [0, 0, 1, 1],
    ...                  [1, 1, 1, 0]], dtype=bool)
    >>> jnp.max(x, axis=1, keepdims=True, initial=0, where=where)
    Array([[4],
           [7],
           [8]], dtype=int32)

    or must be broadcast compatible with input.

    >>> where = jnp.array([[False],
    ...                    [False],
    ...                    [False]])
    >>> jnp.max(x, axis=0, keepdims=True, initial=0, where=where)
    Array([[0, 0, 0, 0]], dtype=int32)
  """
  return _reduce_max(a, axis=_ensure_optional_axes(axis), out=out,
                     keepdims=keepdims, initial=initial, where=where)

