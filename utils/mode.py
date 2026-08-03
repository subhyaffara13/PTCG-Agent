import math


def mode(a, axis=0):
    """
    Returns an array of the modal (most common) value in the passed array.

    Parameters
    ----------
    a : array_like
        n-dimensional array of which to find mode(s).
    axis : int or None, optional
        Axis along which to operate. Default is 0. If None, compute over
        the whole array `a`.

    Returns
    -------
    mode : ndarray
        Array of modal values.
    count : ndarray
        Array of counts for each mode.

    Notes
    -----
    For more details, see `scipy.stats.mode`.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import stats
    >>> from scipy.stats import mstats
    >>> m_arr = np.ma.array([1, 1, 0, 0, 0, 0], mask=[0, 0, 1, 1, 1, 0])
    >>> mstats.mode(m_arr)  # note that most zeros are masked
    ModeResult(mode=array([1.]), count=array([2.]))

    """
    return _mode(a, axis=axis, keepdims=True)


def mode(a, axis=0, nan_policy='propagate', keepdims=False):
    r"""Return an array of the modal (most common) value in the passed array.

    If there is more than one such value, only one is returned.
    The bin-count for the modal bins is also returned.

    Parameters
    ----------
    a : array_like
        Numeric, n-dimensional array of which to find mode(s).
    axis : int or None, optional
        Axis along which to operate. Default is 0. If None, compute over
        the whole array `a`.
    nan_policy : {'propagate', 'raise', 'omit'}, optional
        Defines how to handle when input contains nan.
        The following options are available (default is 'propagate'):

        * 'propagate': treats nan as it would treat any other value
        * 'raise': throws an error
        * 'omit': performs the calculations ignoring nan values

    keepdims : bool, optional
        If set to ``False``, the `axis` over which the statistic is taken
        is consumed (eliminated from the output array). If set to ``True``,
        the `axis` is retained with size one, and the result will broadcast
        correctly against the input array.

    Returns
    -------
    mode : ndarray
        Array of modal values.
    count : ndarray
        Array of counts for each mode.

    Notes
    -----
    The mode  is calculated using `numpy.unique`.
    In NumPy versions 1.21 and after, all NaNs - even those with different
    binary representations - are treated as equivalent and counted as separate
    instances of the same value.

    By convention, the mode of an empty array is NaN, and the associated count
    is zero.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[3, 0, 3, 7],
    ...               [3, 2, 6, 2],
    ...               [1, 7, 2, 8],
    ...               [3, 0, 6, 1],
    ...               [3, 2, 5, 5]])
    >>> from scipy import stats
    >>> stats.mode(a, keepdims=True)
    ModeResult(mode=array([[3, 0, 6, 1]]), count=array([[4, 2, 2, 1]]))

    To get mode of whole array, specify ``axis=None``:

    >>> stats.mode(a, axis=None, keepdims=True)
    ModeResult(mode=[[3]], count=[[5]])
    >>> stats.mode(a, axis=None, keepdims=False)
    ModeResult(mode=3, count=5)

    """
    xp = array_namespace(a)

    # `axis`, `nan_policy`, and `keepdims` are handled by `_axis_nan_policy`
    if not xp.isdtype(a.dtype, 'numeric'):
        message = ("Argument `a` is not recognized as numeric. "
                   "Support for input that cannot be coerced to a numeric "
                   "array was deprecated in SciPy 1.9.0 and removed in SciPy "
                   "1.11.0. Please consider `np.unique`.")
        raise TypeError(message)

    if xp_size(a) == 0:
        NaN = _get_nan(a, xp=xp)
        return ModeResult(*xp.asarray([NaN, 0], dtype=NaN.dtype))

    if a.ndim == 1 and not is_marray(xp):
        vals, cnts = xp.unique_counts(a)
        # in contrast with np.unique, `unique_counts` treats all NaNs as distinct,
        # but we have always grouped them. Replace `cnts` corresponding with NaNs
        # with the number of NaNs.
        mask = xp.isnan(vals)
        cnts = xpx.at(cnts)[mask].set(xp.count_nonzero(mask))
        modes, counts = vals[xp.argmax(cnts)], xp.max(cnts)
        default_int = xp.asarray(1).dtype  # fail slow CI job failed - incorrect dtype
        counts = xp.astype(counts, default_int, copy=False)
        modes = modes[()] if modes.ndim == 0 else modes
        counts = counts[()] if counts.ndim == 0 else counts
        return ModeResult(modes, counts)

    # `axis` is always -1 after the `_axis_nan_policy` decorator
    y = xp.sort(a, axis=-1)

    # Get boolean array of elements that are different from the previous element
    if is_marray(xp):
        # Treat masked elements as NaNs and *don't* count NaNs as equal. Two downsides:
        # - integer arrays are converted to floating point, so some very large distinct
        #   integers will no longer be distinct.
        # - NaNs in the original data *will* be treated as distinct.
        y_data = xp_promote(y.data, force_floating=True, xp=y._xp)
        y_data = y._xp.where(y.mask, y._xp.nan, y_data)
        i = xp.concat([xp.ones(y.shape[:-1] + (1,), dtype=xp.bool),
                      (y_data[..., :-1] != y_data[..., 1:])], axis=-1)
    else:
        i = xp.concat([xp.ones(y.shape[:-1] + (1,), dtype=xp.bool),
                      (y[..., :-1] != y[..., 1:]) & ~xp.isnan(y[..., :-1])], axis=-1)
    # Get linear integer indices of these elements in a raveled array
    indices = xp.arange(xp_size(y), device=xp_device(y))[xp_ravel(i)]
    # The difference between integer indices is the number of repeats
    append = xp.full(indices.shape[:-1] + (1,), xp_size(y), dtype=indices.dtype)
    counts = xp.diff(indices, append=append)
    # Now we form an array of `counts` corresponding with each element of `y`...
    counts = xp.reshape(xp.repeat(counts, counts), y.shape)
    # ... so we can get the argmax of *each slice* separately.
    k = xp.argmax(counts, axis=-1, keepdims=True)
    # Extract the corresponding element/count, and eliminate the reduced dimension
    modes = xp.take_along_axis(y, k, axis=-1)[..., 0]
    counts = xp.take_along_axis(counts, k, axis=-1)[..., 0]
    modes = modes[()] if modes.ndim == 0 else modes
    counts = counts[()] if counts.ndim == 0 else counts
    return ModeResult(modes, counts)


def mode(
    values: ArrayLike, dropna: bool = True, mask: npt.NDArray[np.bool_] | None = None
) -> tuple[np.ndarray, npt.NDArray[np.bool_]] | ExtensionArray:
    """
    Returns the mode(s) of an array.

    Parameters
    ----------
    values : array-like
        Array over which to check for duplicate values.
    dropna : bool, default True
        Don't consider counts of NaN/NaT.

    Returns
    -------
    Union[Tuple[np.ndarray, npt.NDArray[np.bool_]], ExtensionArray]
    """
    values = _ensure_arraylike(values, func_name="mode")
    original = values

    if needs_i8_conversion(values.dtype):
        # Got here with ndarray; dispatch to DatetimeArray/TimedeltaArray.
        values = ensure_wrapped_if_datetimelike(values)
        values = cast("ExtensionArray", values)
        return values._mode(dropna=dropna)

    values = _ensure_data(values)

    npresult, res_mask = htable.mode(values, dropna=dropna, mask=mask)
    if res_mask is None:
        res_mask = np.zeros(npresult.shape, dtype=np.bool_)
    else:
        return npresult, res_mask

    try:
        npresult = safe_sort(npresult)
    except TypeError as err:
        warnings.warn(
            f"Unable to sort modes: {err}",
            stacklevel=find_stack_level(),
        )

    result = _reconstruct_data(npresult, original.dtype, original)
    return result, res_mask


def mode(request):
    return request.param


def mode(request):
    return request.param


def mode(a: ArrayLike, axis: int | None = 0, nan_policy: str = "propagate", keepdims: bool = False) -> ModeResult:
  """Compute the mode (most common value) along an axis of an array.

  JAX implementation of :func:`scipy.stats.mode`.

  Args:
    a: arraylike
    axis: int, default=0. Axis along which to compute the mode.
    nan_policy: str. JAX only supports ``"propagate"``.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.

  Returns:
    A tuple of arrays, ``(mode, count)``. ``mode`` is the array of modal values,
    and ``count`` is the number of times each value appears in the input array.

  Examples:
    >>> x = jnp.array([2, 4, 1, 1, 3, 4, 4, 2, 3])
    >>> mode, count = jax.scipy.stats.mode(x)
    >>> mode, count
    (Array(4, dtype=int32), Array(3, dtype=int32))

    For multi dimensional arrays, ``jax.scipy.stats.mode`` computes the ``mode``
    and the corresponding ``count`` along ``axis=0``:

    >>> x1 = jnp.array([[1, 2, 1, 3, 2, 1],
    ...                 [3, 1, 3, 2, 1, 3],
    ...                 [1, 2, 2, 3, 1, 2]])
    >>> mode, count = jax.scipy.stats.mode(x1)
    >>> mode, count
    (Array([1, 2, 1, 3, 1, 1], dtype=int32), Array([2, 2, 1, 2, 2, 1], dtype=int32))

    If ``axis=1``, ``mode`` and ``count`` will be computed along ``axis 1``.

    >>> mode, count = jax.scipy.stats.mode(x1, axis=1)
    >>> mode, count
    (Array([1, 3, 2], dtype=int32), Array([3, 3, 3], dtype=int32))

    By default, ``jax.scipy.stats.mode`` reduces the dimension of the result.
    To keep the dimensions same as that of the input array, the argument
    ``keepdims`` must be set to ``True``.

    >>> mode, count = jax.scipy.stats.mode(x1, axis=1, keepdims=True)
    >>> mode, count
    (Array([[1],
           [3],
           [2]], dtype=int32), Array([[3],
           [3],
           [3]], dtype=int32))
  """
  check_arraylike("mode", a)
  x = jnp.atleast_1d(a)

  if nan_policy not in ["propagate", "omit", "raise"]:
    raise ValueError(
      f"Illegal nan_policy value {nan_policy!r}; expected one of "
      "{'propagate', 'omit', 'raise'}"
    )
  if nan_policy == "omit":
    # TODO: return answer without nans included.
    raise NotImplementedError(
      f"Logic for `nan_policy` of {nan_policy} is not implemented"
    )
  if nan_policy == "raise":
    raise NotImplementedError(
      "In order to best JIT compile `mode`, we cannot know whether `x` contains nans. "
      "Please check if nans exist in `x` outside of the `mode` function."
    )
  if axis is not None:
    axis = canonicalize_axis(axis, x.ndim)

  input_shape = x.shape
  if keepdims:
    if axis is None:
      output_shape = tuple(1 for i in input_shape)
    else:
      output_shape = tuple(1 if i == axis else s for i, s in enumerate(input_shape))
  else:
    if axis is None:
      output_shape = ()
    else:
      output_shape = tuple(s for i, s in enumerate(input_shape) if i != axis)

  if axis is None:
    axis = 0
    x = x.ravel()

  def _mode_helper(x: Array) -> tuple[Array, Array]:
    """Helper function to return mode and count of a given array."""
    if x.size == 0:
      return (jnp.array(np.nan, dtype=dtypes.default_float_dtype()),
              jnp.array(0, dtype=dtypes.default_float_dtype()))
    else:
      vals, counts = jnp.unique(x, return_counts=True, size=x.size)
      return vals[jnp.argmax(counts)], counts.max()

  x = jnp.moveaxis(x, axis, 0)
  x = x.reshape(x.shape[0], math.prod(x.shape[1:]))
  vals, counts = api.vmap(_mode_helper, in_axes=1)(x)
  return ModeResult(vals.reshape(output_shape), counts.reshape(output_shape))

