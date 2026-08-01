
def nanmedian(
    values: np.ndarray, *, axis: AxisInt | None = None, skipna: bool = True, mask=None
) -> float | np.ndarray:
    """
    Parameters
    ----------
    values : ndarray
    axis : int, optional
    skipna : bool, default True
    mask : ndarray[bool], optional
        nan-mask if known

    Returns
    -------
    result : float | ndarray
        Unless input is a float array, in which case use the same
        precision as the input array.

    Examples
    --------
    >>> from pandas.core import nanops
    >>> s = pd.Series([1, np.nan, 2, 2])
    >>> nanops.nanmedian(s.values)
    2.0

    >>> s = pd.Series([np.nan, np.nan, np.nan])
    >>> nanops.nanmedian(s.values)
    nan
    """
    # for floats without mask, the data already uses NaN as missing value
    # indicator, and `mask` will be calculated from that below -> in those
    # cases we never need to set NaN to the masked values
    using_nan_sentinel = values.dtype.kind == "f" and mask is None

    def get_median(x: np.ndarray, _mask=None):
        if _mask is None:
            _mask = notna(x)
        else:
            _mask = ~_mask
        if not skipna and not _mask.all():
            return np.nan
        with warnings.catch_warnings():
            # Suppress RuntimeWarning about All-NaN slice
            warnings.filterwarnings(
                "ignore", "All-NaN slice encountered", RuntimeWarning
            )
            warnings.filterwarnings("ignore", "Mean of empty slice", RuntimeWarning)
            res = np.nanmedian(x[_mask])
        return res

    dtype = values.dtype
    values, mask = _get_values(values, skipna, mask=mask, fill_value=None)
    if values.dtype.kind != "f":
        if values.dtype == object:
            # GH#34671 avoid casting strings to numeric
            inferred = lib.infer_dtype(values)
            if inferred in ["string", "mixed"]:
                raise TypeError(f"Cannot convert {values} to numeric")
        try:
            values = values.astype("f8")
        except ValueError as err:
            # e.g. "could not convert string to float: 'a'"
            raise TypeError(str(err)) from err
    if not using_nan_sentinel and mask is not None:
        if not values.flags.writeable:
            values = values.copy()
        values[mask] = np.nan

    notempty = values.size

    res: float | np.ndarray

    # an array from a frame
    if values.ndim > 1 and axis is not None:
        # there's a non-empty array to apply over otherwise numpy raises
        if notempty:
            if not skipna:
                res = np.apply_along_axis(get_median, axis, values)

            else:
                # fastpath for the skipna case
                with warnings.catch_warnings():
                    # Suppress RuntimeWarning about All-NaN slice
                    warnings.filterwarnings(
                        "ignore", "All-NaN slice encountered", RuntimeWarning
                    )
                    if (values.shape[1] == 1 and axis == 0) or (
                        values.shape[0] == 1 and axis == 1
                    ):
                        # GH52788: fastpath when squeezable, nanmedian for 2D array slow
                        res = np.nanmedian(np.squeeze(values), keepdims=True)
                    else:
                        res = np.nanmedian(values, axis=axis)

        else:
            # must return the correct shape, but median is not defined for the
            # empty set so return nans of shape "everything but the passed axis"
            # since "axis" is where the reduction would occur if we had a nonempty
            # array
            res = _get_empty_reduction_result(values.shape, axis)

    else:
        # otherwise return a scalar value
        res = get_median(values, mask) if notempty else np.nan
    return _wrap_results(res, dtype)


def nanmedian(a, axis=None, out=None, overwrite_input=False, keepdims=np._NoValue):
    """
    Compute the median along the specified axis, while ignoring NaNs.

    Returns the median of the array elements.

    Parameters
    ----------
    a : array_like
        Input array or object that can be converted to an array.
    axis : {int, sequence of int, None}, optional
        Axis or axes along which the medians are computed. The default
        is to compute the median along a flattened version of the array.
        A sequence of axes is supported since version 1.9.0.
    out : ndarray, optional
        Alternative output array in which to place the result. It must
        have the same shape and buffer length as the expected output,
        but the type (of the output) will be cast if necessary.
    overwrite_input : bool, optional
       If True, then allow use of memory of input array `a` for
       calculations. The input array will be modified by the call to
       `median`. This will save memory when you do not need to preserve
       the contents of the input array. Treat the input as undefined,
       but it will probably be fully or partially sorted. Default is
       False. If `overwrite_input` is ``True`` and `a` is not already an
       `ndarray`, an error will be raised.
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the original `a`.

        If this is anything but the default value it will be passed
        through (in the special case of an empty array) to the
        `mean` function of the underlying array.  If the array is
        a sub-class and `mean` does not have the kwarg `keepdims` this
        will raise a RuntimeError.

    Returns
    -------
    median : ndarray
        A new array holding the result. If the input contains integers
        or floats smaller than ``float64``, then the output data-type is
        ``np.float64``.  Otherwise, the data-type of the output is the
        same as that of the input. If `out` is specified, that array is
        returned instead.

    See Also
    --------
    mean, median, percentile

    Notes
    -----
    Given a vector ``V`` of length ``N``, the median of ``V`` is the
    middle value of a sorted copy of ``V``, ``V_sorted`` - i.e.,
    ``V_sorted[(N-1)/2]``, when ``N`` is odd and the average of the two
    middle values of ``V_sorted`` when ``N`` is even.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[10.0, 7, 4], [3, 2, 1]])
    >>> a[0, 1] = np.nan
    >>> a
    array([[10., nan,  4.],
           [ 3.,  2.,  1.]])
    >>> np.median(a)
    np.float64(nan)
    >>> np.nanmedian(a)
    3.0
    >>> np.nanmedian(a, axis=0)
    array([6.5, 2. , 2.5])
    >>> np.median(a, axis=1)
    array([nan,  2.])
    >>> b = a.copy()
    >>> np.nanmedian(b, axis=1, overwrite_input=True)
    array([7.,  2.])
    >>> assert not np.all(a==b)
    >>> b = a.copy()
    >>> np.nanmedian(b, axis=None, overwrite_input=True)
    3.0
    >>> assert not np.all(a==b)

    """
    a = np.asanyarray(a)
    # apply_along_axis in _nanmedian doesn't handle empty arrays well,
    # so deal them upfront
    if a.size == 0:
        return np.nanmean(a, axis, out=out, keepdims=keepdims)

    return fnb._ureduce(a, func=_nanmedian, keepdims=keepdims,
                        axis=axis, out=out,
                        overwrite_input=overwrite_input)


def nanmedian(a: ArrayLike, axis: int | tuple[int, ...] | None = None,
              out: None = None, overwrite_input: bool = False,
              keepdims: bool = False) -> Array:
  r"""Return the median of array elements along a given axis, ignoring NaNs.

  JAX implementation of :func:`numpy.nanmedian`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      median to be computed. If None, median is computed for the flattened array.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    out: Unused by JAX.
    overwrite_input: Unused by JAX.

  Returns:
    An array containing the median along the given axis, ignoring NaNs. If all
    elements along the given axis are NaNs, returns ``nan``.

  See also:
    - :func:`jax.numpy.nanmean`: Compute the mean of array elements over a given
      axis, ignoring NaNs.
    - :func:`jax.numpy.nanmax`: Compute the maximum of array elements over given
      axis, ignoring NaNs.
    - :func:`jax.numpy.nanmin`: Compute the minimum of array elements over given
      axis, ignoring NaNs.

  Examples:
    By default, the median is computed for the flattened array.

    >>> nan = jnp.nan
    >>> x = jnp.array([[2, nan, 7, nan],
    ...                [nan, 5, 9, 2],
    ...                [6, 1, nan, 3]])
    >>> jnp.nanmedian(x)
    Array(4., dtype=float32)

    If ``axis=1``, the median is computed along axis 1.

    >>> jnp.nanmedian(x, axis=1)
    Array([4.5, 5. , 3. ], dtype=float32)

    If ``keepdims=True``, ``ndim`` of the output is equal to that of the input.

    >>> jnp.nanmedian(x, axis=1, keepdims=True)
    Array([[4.5],
           [5. ],
           [3. ]], dtype=float32)
  """
  a = ensure_arraylike("nanmedian", a)
  return nanquantile(a, 0.5, axis=axis, out=out,
                     overwrite_input=overwrite_input, keepdims=keepdims,
                     method='midpoint')

