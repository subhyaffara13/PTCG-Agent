
def nanvar(
    values: np.ndarray,
    *,
    axis: AxisInt | None = None,
    skipna: bool = True,
    ddof: int = 1,
    mask=None,
):
    """
    Compute the variance along given axis while ignoring NaNs

    Parameters
    ----------
    values : ndarray
    axis : int, optional
    skipna : bool, default True
    ddof : int, default 1
        Delta Degrees of Freedom. The divisor used in calculations is N - ddof,
        where N represents the number of elements.
    mask : ndarray[bool], optional
        nan-mask if known

    Returns
    -------
    result : float
        Unless input is a float array, in which case use the same
        precision as the input array.

    Examples
    --------
    >>> from pandas.core import nanops
    >>> s = pd.Series([1, np.nan, 2, 3])
    >>> nanops.nanvar(s.values)
    1.0
    """
    dtype = values.dtype
    mask = _maybe_get_mask(values, skipna, mask)
    if dtype.kind in "iu":
        values = values.astype("f8")
        if mask is not None:
            values[mask] = np.nan
    elif dtype.kind == "c":
        # https://en.wikipedia.org/wiki/Complex_random_variable#Variance_and_pseudo-variance
        # The variance is equal to the sum of
        # the variances of the real and imaginary part of the complex random variable.
        return nanvar(
            values.real, axis=axis, skipna=skipna, ddof=ddof, mask=mask
        ) + nanvar(values.imag, axis=axis, skipna=skipna, ddof=ddof, mask=mask)

    if values.dtype.kind == "f":
        count, d = _get_counts_nanvar(values.shape, mask, axis, ddof, values.dtype)
    else:
        count, d = _get_counts_nanvar(values.shape, mask, axis, ddof)

    if skipna and mask is not None:
        values = values.copy()
        np.putmask(values, mask, 0)

    # xref GH10242
    # Compute variance via two-pass algorithm, which is stable against
    # cancellation errors and relatively accurate for small numbers of
    # observations.
    #
    # See https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance
    avg = _ensure_numeric(values.sum(axis=axis, dtype=np.float64)) / count
    if axis is not None:
        avg = np.expand_dims(avg, axis)

    sqr = _ensure_numeric((avg - values) ** 2)
    if mask is not None:
        np.putmask(sqr, mask, 0)
    result = sqr.sum(axis=axis, dtype=np.float64) / d

    # Return variance as np.float64 (the datatype used in the accumulator),
    # unless we were dealing with a float array, in which case use the same
    # precision as the original values array.
    if dtype.kind == "f":
        result = result.astype(dtype, copy=False)
    return result


def nanvar(a, axis=None, dtype=None, out=None, ddof=0, keepdims=np._NoValue,
           *, where=np._NoValue, mean=np._NoValue, correction=np._NoValue):
    """
    Compute the variance along the specified axis, while ignoring NaNs.

    Returns the variance of the array elements, a measure of the spread of
    a distribution.  The variance is computed for the flattened array by
    default, otherwise over the specified axis.

    For all-NaN slices or slices with zero degrees of freedom, NaN is
    returned and a `RuntimeWarning` is raised.

    Parameters
    ----------
    a : array_like
        Array containing numbers whose variance is desired.  If `a` is not an
        array, a conversion is attempted.
    axis : {int, tuple of int, None}, optional
        Axis or axes along which the variance is computed.  The default is to compute
        the variance of the flattened array.
    dtype : data-type, optional
        Type to use in computing the variance.  For arrays of integer type
        the default is `float64`; for arrays of float types it is the same as
        the array type.
    out : ndarray, optional
        Alternate output array in which to place the result.  It must have
        the same shape as the expected output, but the type is cast if
        necessary.
    ddof : {int, float}, optional
        "Delta Degrees of Freedom": the divisor used in the calculation is
        ``N - ddof``, where ``N`` represents the number of non-NaN
        elements. By default `ddof` is zero.
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the original `a`.
    where : array_like of bool, optional
        Elements to include in the variance. See `~numpy.ufunc.reduce` for
        details.

        .. versionadded:: 1.22.0

    mean : array_like, optional
        Provide the mean to prevent its recalculation. The mean should have
        a shape as if it was calculated with ``keepdims=True``.
        The axis for the calculation of the mean should be the same as used in
        the call to this var function.

        .. versionadded:: 2.0.0

    correction : {int, float}, optional
        Array API compatible name for the ``ddof`` parameter. Only one of them
        can be provided at the same time.

        .. versionadded:: 2.0.0

    Returns
    -------
    variance : ndarray, see dtype parameter above
        If `out` is None, return a new array containing the variance,
        otherwise return a reference to the output array. If ddof is >= the
        number of non-NaN elements in a slice or the slice contains only
        NaNs, then the result for that slice is NaN.

    See Also
    --------
    std : Standard deviation
    mean : Average
    var : Variance while not ignoring NaNs
    nanstd, nanmean
    :ref:`ufuncs-output-type`

    Notes
    -----
    The variance is the average of the squared deviations from the mean,
    i.e.,  ``var = mean(abs(x - x.mean())**2)``.

    The mean is normally calculated as ``x.sum() / N``, where ``N = len(x)``.
    If, however, `ddof` is specified, the divisor ``N - ddof`` is used
    instead.  In standard statistical practice, ``ddof=1`` provides an
    unbiased estimator of the variance of a hypothetical infinite
    population.  ``ddof=0`` provides a maximum likelihood estimate of the
    variance for normally distributed variables.

    Note that for complex numbers, the absolute value is taken before
    squaring, so that the result is always real and nonnegative.

    For floating-point input, the variance is computed using the same
    precision the input has.  Depending on the input data, this can cause
    the results to be inaccurate, especially for `float32` (see example
    below).  Specifying a higher-accuracy accumulator using the ``dtype``
    keyword can alleviate this issue.

    For this function to work on sub-classes of ndarray, they must define
    `sum` with the kwarg `keepdims`

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1, np.nan], [3, 4]])
    >>> np.nanvar(a)
    1.5555555555555554
    >>> np.nanvar(a, axis=0)
    array([1.,  0.])
    >>> np.nanvar(a, axis=1)
    array([0.,  0.25])  # may vary

    """
    arr, mask = _replace_nan(a, 0)
    if mask is None:
        return np.var(arr, axis=axis, dtype=dtype, out=out, ddof=ddof,
                      keepdims=keepdims, where=where, mean=mean,
                      correction=correction)

    if dtype is not None:
        dtype = np.dtype(dtype)
    if dtype is not None and not issubclass(dtype.type, np.inexact):
        raise TypeError("If a is inexact, then dtype must be inexact")
    if out is not None and not issubclass(out.dtype.type, np.inexact):
        raise TypeError("If a is inexact, then out must be inexact")

    if correction != np._NoValue:
        if ddof != 0:
            raise ValueError(
                "ddof and correction can't be provided simultaneously."
            )
        else:
            ddof = correction

    # Compute mean
    if type(arr) is np.matrix:
        _keepdims = np._NoValue
    else:
        _keepdims = True

    cnt = np.sum(~mask, axis=axis, dtype=np.intp, keepdims=_keepdims,
                     where=where)

    if mean is not np._NoValue:
        avg = mean
    else:
        # we need to special case matrix for reverse compatibility
        # in order for this to work, these sums need to be called with
        # keepdims=True, however matrix now raises an error in this case, but
        # the reason that it drops the keepdims kwarg is to force keepdims=True
        # so this used to work by serendipity.
        avg = np.sum(arr, axis=axis, dtype=dtype,
                     keepdims=_keepdims, where=where)
        avg = _divide_by_count(avg, cnt)

    # Compute squared deviation from mean.
    np.subtract(arr, avg, out=arr, casting='unsafe', where=where)
    arr = _copyto(arr, 0, mask)
    if issubclass(arr.dtype.type, np.complexfloating):
        sqr = np.multiply(arr, arr.conj(), out=arr, where=where).real
    else:
        sqr = np.multiply(arr, arr, out=arr, where=where)

    # Compute variance.
    var = np.sum(sqr, axis=axis, dtype=dtype, out=out, keepdims=keepdims,
                 where=where)

    # Precaution against reduced object arrays
    try:
        var_ndim = var.ndim
    except AttributeError:
        var_ndim = np.ndim(var)
    if var_ndim < cnt.ndim:
        # Subclasses of ndarray may ignore keepdims, so check here.
        cnt = cnt.squeeze(axis)
    dof = cnt - ddof
    var = _divide_by_count(var, dof)

    isbad = (dof <= 0)
    if np.any(isbad):
        warnings.warn("Degrees of freedom <= 0 for slice.", RuntimeWarning,
                      stacklevel=2)
        # NaN, inf, or negative numbers are all possible bad
        # values, so explicitly replace them with NaN.
        var = _copyto(var, np.nan, isbad)
    return var


def nanvar(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None, out: None = None,
           ddof: int = 0, keepdims: bool = False,
           where: ArrayLike | None = None, mean: ArrayLike | None = None) -> Array:
  r"""Compute the variance of array elements along a given axis, ignoring NaNs.

  JAX implementation of :func:`numpy.nanvar`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      variance is computed. If None, variance is computed along flattened array.
    dtype: The type of the output array. Default=None.
    ddof: int, default=0. Degrees of freedom. The divisor in the variance computation
      is ``N-ddof``, ``N`` is number of elements along given axis.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    where: optional, boolean array, default=None. The elements to be used in the
      variance. Array should be broadcast compatible to the input.
    mean: optional, mean of the input array, computed along the given axis.
      If provided, it will be used to compute the variance instead of
      computing it from the input array. If specified, mean must be broadcast-compatible
      with the input array. In the general case, this can be achieved by computing the mean with
      ``keepdims=True`` and ``axis`` matching this function's ``axis`` argument.
    out: Unused by JAX.

  Returns:
    An array containing the variance of array elements along specified axis. If
    all elements along the given axis are NaNs, returns ``nan``.

  See also:
    - :func:`jax.numpy.nanmean`: Compute the mean of array elements over a given
      axis, ignoring NaNs.
    - :func:`jax.numpy.nanstd`: Computed the standard deviation of a given axis,
      ignoring NaNs.
    - :func:`jax.numpy.var`: Compute the variance of array elements along a given
      axis.

  Examples:
    By default, ``jnp.nanvar`` computes the variance along all axes.

    >>> nan = jnp.nan
    >>> x = jnp.array([[1, nan, 4, 3],
    ...                [nan, 2, nan, 9],
    ...                [4, 8, 6, nan]])
    >>> jnp.nanvar(x)
    Array(6.984375, dtype=float32)

    If ``axis=1``, variance is computed along axis 1.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.nanvar(x, axis=1))
    [ 1.56 12.25  2.67]

    To preserve the dimensions of input, you can set ``keepdims=True``.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.nanvar(x, axis=1, keepdims=True))
    [[ 1.56]
     [12.25]
     [ 2.67]]

    If ``ddof=1``:

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.nanvar(x, axis=1, keepdims=True, ddof=1))
    [[ 2.33]
     [24.5 ]
     [ 4.  ]]

    To include specific elements of the array to compute variance, you can use
    ``where``.

    >>> where = jnp.array([[1, 0, 1, 0],
    ...                    [0, 1, 1, 0],
    ...                    [1, 1, 0, 1]], dtype=bool)
    >>> jnp.nanvar(x, axis=1, keepdims=True, where=where)
    Array([[2.25],
           [0.  ],
           [4.  ]], dtype=float32)
  """
  a = ensure_arraylike("nanvar", a)
  where = check_where("nanvar", where)
  if dtype is not None:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "nanvar")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.nanvar is not supported.")
  return _nanvar(a, axis=axis, dtype=dtype, out=out, ddof=ddof, keepdims=keepdims, where=where, a_mean=mean)

