
def min(g: jit_utils.GraphContext, self, dim_or_y=None, keepdim=None):
    return symbolic_helper._min_helper(g, self, dim_or_y, keepdim)


def min(g: jit_utils.GraphContext, self, dim_or_y=None, keepdim=None):
    # torch.min(input, other)
    if keepdim is None and dim_or_y is not None:
        warnings.warn(
            "Multidirectional broadcasting is not supported in opset 7. "
            "This might cause the onnx model to be incorrect, if inputs to min operators "
            "have different shapes",
            stacklevel=2,
        )
    return opset9.min(g, self, dim_or_y, keepdim)


def min(g: jit_utils.GraphContext, self, dim_or_y=None, keepdim=None):
    return symbolic_helper._min_helper(g, self, dim_or_y, keepdim)


def min(x: Array, /, *, axis: int | tuple[int, ...] |None = None, keepdims: bool = False) -> Array:
    # https://github.com/pytorch/pytorch/issues/29137
    if axis == ():
        return torch.clone(x)
    return torch.amin(x, axis, keepdims=keepdims)


def min(
    values: np.ndarray,
    mask: npt.NDArray[np.bool_],
    *,
    skipna: bool = True,
    axis: AxisInt | None = None,
):
    return _minmax(np.min, values=values, mask=mask, skipna=skipna, axis=axis)


def min(obj, axis=None, out=None, fill_value=None, keepdims=np._NoValue):
    kwargs = {} if keepdims is np._NoValue else {'keepdims': keepdims}

    try:
        return obj.min(axis=axis, fill_value=fill_value, out=out, **kwargs)
    except (AttributeError, TypeError):
        # If obj doesn't have a min method, or if the method doesn't accept a
        # fill_value argument
        return asanyarray(obj).min(axis=axis, fill_value=fill_value,
                                   out=out, **kwargs)


def min(a, axis=None, out=None, keepdims=np._NoValue, initial=np._NoValue,
        where=np._NoValue):
    """
    Return the minimum of an array or minimum along an axis.

    Parameters
    ----------
    a : array_like
        Input data.
    axis : None or int or tuple of ints, optional
        Axis or axes along which to operate.  By default, flattened input is
        used.

        If this is a tuple of ints, the minimum is selected over multiple axes,
        instead of a single axis or all the axes as before.
    out : ndarray, optional
        Alternative output array in which to place the result.  Must
        be of the same shape and buffer length as the expected output.
        See :ref:`ufuncs-output-type` for more details.

    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the input array.

        If the default value is passed, then `keepdims` will not be
        passed through to the ``min`` method of sub-classes of
        `ndarray`, however any non-default value will be.  If the
        sub-class' method does not implement `keepdims` any
        exceptions will be raised.

    initial : scalar, optional
        The maximum value of an output element. Must be present to allow
        computation on empty slice. See `~numpy.ufunc.reduce` for details.

    where : array_like of bool, optional
        Elements to compare for the minimum. See `~numpy.ufunc.reduce`
        for details.

    Returns
    -------
    min : ndarray or scalar
        Minimum of `a`. If `axis` is None, the result is a scalar value.
        If `axis` is an int, the result is an array of dimension
        ``a.ndim - 1``.  If `axis` is a tuple, the result is an array of
        dimension ``a.ndim - len(axis)``.

    See Also
    --------
    max :
        The maximum value of an array along a given axis, propagating any NaNs.
    nanmin :
        The minimum value of an array along a given axis, ignoring any NaNs.
    minimum :
        Element-wise minimum of two arrays, propagating any NaNs.
    fmin :
        Element-wise minimum of two arrays, ignoring any NaNs.
    argmin :
        Return the indices of the minimum values.

    nanmax, maximum, fmax

    Notes
    -----
    NaN values are propagated, that is if at least one item is NaN, the
    corresponding min value will be NaN as well. To ignore NaN values
    (MATLAB behavior), please use nanmin.

    Don't use `~numpy.min` for element-wise comparison of 2 arrays; when
    ``a.shape[0]`` is 2, ``minimum(a[0], a[1])`` is faster than
    ``min(a, axis=0)``.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.arange(4).reshape((2,2))
    >>> a
    array([[0, 1],
           [2, 3]])
    >>> np.min(a)           # Minimum of the flattened array
    0
    >>> np.min(a, axis=0)   # Minima along the first axis
    array([0, 1])
    >>> np.min(a, axis=1)   # Minima along the second axis
    array([0, 2])
    >>> np.min(a, where=[False, True], initial=10, axis=0)
    array([10,  1])

    >>> b = np.arange(5, dtype=np.float64)
    >>> b[2] = np.nan
    >>> np.min(b)
    np.float64(nan)
    >>> np.min(b, where=~np.isnan(b), initial=10)
    0.0
    >>> np.nanmin(b)
    0.0

    >>> np.min([[-50], [10]], axis=-1, initial=0)
    array([-50,   0])

    Notice that the initial value is used as one of the elements for which the
    minimum is determined, unlike for the default argument Python's max
    function, which is only used for empty iterables.

    Notice that this isn't the same as Python's ``default`` argument.

    >>> np.min([6], initial=5)
    5
    >>> min([6], default=5)
    6
    """
    return _wrapreduction(a, np.minimum, 'min', axis, None, out,
                          keepdims=keepdims, initial=initial, where=where)


def MIN(x, y):
    if mpf_le(x, y):
        return x
    return y


def min(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise minimum: :math:`\mathrm{min}(x, y)`

  This function lowers directly to the `stablehlo.minimum`_ operation for
  non-complex inputs. For complex numbers, this uses a lexicographic
  comparison on the `(real, imaginary)` pairs.

  Args:
    x, y: Input arrays. Must have matching dtypes. If neither is a scalar,
      ``x`` and ``y`` must have the same rank and be broadcast compatible.

  Returns:
    An array of the same dtype as ``x`` and ``y`` containing the elementwise
    minimum.

  See also:
    - :func:`jax.numpy.minimum`: more flexibly NumPy-style minimum.
    - :func:`jax.lax.reduce_min`: minimum along an axis of an array.
    - :func:`jax.lax.max`: elementwise maximum.

  .. _stablehlo.minimum: https://openxla.org/stablehlo/spec#minimum
  """
  x, y = core.auto_insert_reshard(x, y)
  return min_p.bind(x, y)


def min(a: ArrayLike, axis: Axis = None, out: None = None,
        keepdims: bool = False, initial: ArrayLike | None = None,
        where: ArrayLike | None = None) -> Array:
  r"""Return the minimum of array elements along a given axis.

  JAX implementation of :func:`numpy.min`.

  Args:
    a: Input array.
    axis: int or array, default=None. Axis along which the minimum to be computed.
      If None, the minimum is computed along all the axes.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    initial: int or array, Default=None. Initial value for the minimum.
    where: int or array, default=None. The elements to be used in the minimum.
      Array should be broadcast compatible to the input. ``initial`` must be
      specified when ``where`` is used.
    out: Unused by JAX.

  Returns:
    An array of minimum values along the given axis.

  See also:
    - :func:`jax.numpy.max`: Compute the maximum of array elements along a given
      axis.
    - :func:`jax.numpy.sum`: Compute the sum of array elements along a given axis.
    - :func:`jax.numpy.prod`: Compute the product of array elements along a given
      axis.

  Examples:
    By default, the minimum is computed along all the axes.

    >>> x = jnp.array([[2, 5, 1, 6],
    ...                [3, -7, -2, 4],
    ...                [8, -4, 1, -3]])
    >>> jnp.min(x)
    Array(-7, dtype=int32)

    If ``axis=1``, the minimum is computed along axis 1.

    >>> jnp.min(x, axis=1)
    Array([ 1, -7, -4], dtype=int32)

    If ``keepdims=True``, ``ndim`` of the output will be same of that of the input.

    >>> jnp.min(x, axis=1, keepdims=True)
    Array([[ 1],
           [-7],
           [-4]], dtype=int32)

    To include only specific elements in computing the minimum, you can use
    ``where``. ``where`` can either have same dimension as input.

    >>> where=jnp.array([[1, 0, 1, 0],
    ...                  [0, 0, 1, 1],
    ...                  [1, 1, 1, 0]], dtype=bool)
    >>> jnp.min(x, axis=1, keepdims=True, initial=0, where=where)
    Array([[ 0],
           [-2],
           [-4]], dtype=int32)

    or must be broadcast compatible with input.

    >>> where = jnp.array([[False],
    ...                    [False],
    ...                    [False]])
    >>> jnp.min(x, axis=0, keepdims=True, initial=0, where=where)
    Array([[0, 0, 0, 0]], dtype=int32)
  """
  return _reduce_min(a, axis=_ensure_optional_axes(axis), out=out,
                     keepdims=keepdims, initial=initial, where=where)

