
def std(
    input: Tensor | MaskedTensor,
    dim: DimOrDims = None,
    unbiased: bool | None = None,
    *,
    correction: int | None = None,
    keepdim: bool | None = False,
    dtype: DType | None = None,
    mask: Tensor | None = None,
) -> Tensor:
    """\
{reduction_signature}
{reduction_descr}
The identity value of sample standard deviation operation is undefined. The
elements of output tensor with strided layout, that correspond to
fully masked-out elements, have ``nan`` values.
{reduction_args}
{reduction_example}"""
    return _std_var(
        input=input,
        dim=dim,
        unbiased=unbiased,
        correction_opt=correction,
        keepdim=keepdim,
        dtype=dtype,
        mask=mask,
        take_sqrt=True,
    )


def std(
    a: ArrayLike,
    axis: AxisLike = None,
    dtype: DTypeLike | None = None,
    out: OutArray | None = None,
    ddof=0,
    keepdims: KeepDims = False,
    *,
    where: NotImplementedType = None,
):
    in_dtype = dtype
    dtype = _atleast_float(dtype, a.dtype)
    tensor = _util.cast_if_needed(a, dtype)
    result = tensor.std(dim=axis, correction=ddof)
    return _util.cast_if_needed(result, in_dtype)


def std(
    a: TensorLikeType,
    dim: int | None | list[int] = None,
    unbiased: bool | None = None,
    keepdim: bool = False,
    *,
    correction: NumberType | None = None,
) -> TensorLikeType:
    dim, unbiased = _dim_var_dispatch(dim, unbiased)
    correction = utils.set_correction(unbiased, correction)

    opmath_dtype, dtype = utils.reduction_dtypes(
        a, REDUCTION_OUTPUT_TYPE_KIND.COMPLEX_TO_FLOAT
    )
    a = _maybe_convert_to_dtype(a, opmath_dtype)
    a_var = torch.var(a, dim, correction=correction, keepdim=keepdim)
    a_std = torch.sqrt(a_var)
    if dtype is None:
        raise AssertionError("dtype should not be None after reduction_dtypes")
    return _maybe_convert_to_dtype(a_std, dtype)


def std(g: jit_utils.GraphContext, input, *args):
    var, _ = var_mean(g, input, *args)
    return g.op("Sqrt", var)


def std(
    x: Array,
    /,
    xp: Namespace,
    *,
    axis: int | tuple[int, ...] | None = None,
    correction: float = 0.0,  # correction instead of ddof
    keepdims: bool = False,
    **kwargs: object,
) -> Array:
    return xp.std(x, axis=axis, ddof=correction, keepdims=keepdims, **kwargs)


def std(x: Array,
        /,
        *,
        axis: int | tuple[int, ...] | None = None,
        correction: float = 0.0,
        keepdims: bool = False,
        **kwargs: object) -> Array:
    # Note, float correction is not supported
    # https://github.com/pytorch/pytorch/issues/61492. We don't try to
    # implement it here for now.

    if isinstance(correction, float):
        _correction = int(correction)
        if correction != _correction:
            raise NotImplementedError("float correction in torch std() is not yet supported")
    else:
        _correction = correction

    # https://github.com/pytorch/pytorch/issues/29137
    if axis == ():
        return torch.zeros_like(x)
    if isinstance(axis, int):
        axis = (axis,)
    if axis is None:
        # torch doesn't support keepdims with axis=None
        # (https://github.com/pytorch/pytorch/issues/71209)
        res = torch.std(x, tuple(range(x.ndim)), correction=_correction, **kwargs)
        res = _axis_none_keepdims(res, x.ndim, keepdims)
        return res
    return torch.std(x, axis, correction=_correction, keepdims=keepdims, **kwargs)


def std(
    values: np.ndarray,
    mask: npt.NDArray[np.bool_],
    *,
    skipna: bool = True,
    axis: AxisInt | None = None,
    ddof: int = 1,
):
    if not values.size or mask.all():
        return libmissing.NA

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        return _reductions(
            np.std, values=values, mask=mask, skipna=skipna, axis=axis, ddof=ddof
        )


def std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=np._NoValue, *,
        where=np._NoValue, mean=np._NoValue, correction=np._NoValue):
    r"""
    Compute the standard deviation along the specified axis.

    Returns the standard deviation, a measure of the spread of a distribution,
    of the array elements. The standard deviation is computed for the
    flattened array by default, otherwise over the specified axis.

    Parameters
    ----------
    a : array_like
        Calculate the standard deviation of these values.
    axis : None or int or tuple of ints, optional
        Axis or axes along which the standard deviation is computed. The
        default is to compute the standard deviation of the flattened array.
        If this is a tuple of ints, a standard deviation is performed over
        multiple axes, instead of a single axis or all the axes as before.
    dtype : dtype, optional
        Type to use in computing the standard deviation. For arrays of
        integer type the default is float64, for arrays of float types it is
        the same as the array type.
    out : ndarray, optional
        Alternative output array in which to place the result. It must have
        the same shape as the expected output but the type (of the calculated
        values) will be cast if necessary.
        See :ref:`ufuncs-output-type` for more details.
    ddof : {int, float}, optional
        Means Delta Degrees of Freedom.  The divisor used in calculations
        is ``N - ddof``, where ``N`` represents the number of elements.
        By default `ddof` is zero. See Notes for details about use of `ddof`.
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the input array.

        If the default value is passed, then `keepdims` will not be
        passed through to the `std` method of sub-classes of
        `ndarray`, however any non-default value will be.  If the
        sub-class' method does not implement `keepdims` any
        exceptions will be raised.
    where : array_like of bool, optional
        Elements to include in the standard deviation.
        See `~numpy.ufunc.reduce` for details.

        .. versionadded:: 1.20.0

    mean : array_like, optional
        Provide the mean to prevent its recalculation. The mean should have
        a shape as if it was calculated with ``keepdims=True``.
        The axis for the calculation of the mean should be the same as used in
        the call to this std function.

        .. versionadded:: 2.0.0

    correction : {int, float}, optional
        Array API compatible name for the ``ddof`` parameter. Only one of them
        can be provided at the same time.

        .. versionadded:: 2.0.0

    Returns
    -------
    standard_deviation : ndarray, see dtype parameter above.
        If `out` is None, return a new array containing the standard deviation,
        otherwise return a reference to the output array.

    See Also
    --------
    var, mean, nanmean, nanstd, nanvar
    :ref:`ufuncs-output-type`

    Notes
    -----
    There are several common variants of the array standard deviation
    calculation. Assuming the input `a` is a one-dimensional NumPy array
    and ``mean`` is either provided as an argument or computed as
    ``a.mean()``, NumPy computes the standard deviation of an array as::

        N = len(a)
        d2 = abs(a - mean)**2  # abs is for complex `a`
        var = d2.sum() / (N - ddof)  # note use of `ddof`
        std = var**0.5

    Different values of the argument `ddof` are useful in different
    contexts. NumPy's default ``ddof=0`` corresponds with the expression:

    .. math::

        \sqrt{\frac{\sum_i{|a_i - \bar{a}|^2 }}{N}}

    which is sometimes called the "population standard deviation" in the field
    of statistics because it applies the definition of standard deviation to
    `a` as if `a` were a complete population of possible observations.

    Many other libraries define the standard deviation of an array
    differently, e.g.:

    .. math::

        \sqrt{\frac{\sum_i{|a_i - \bar{a}|^2 }}{N - 1}}

    In statistics, the resulting quantity is sometimes called the "sample
    standard deviation" because if `a` is a random sample from a larger
    population, this calculation provides the square root of an unbiased
    estimate of the variance of the population. The use of :math:`N-1` in the
    denominator is often called "Bessel's correction" because it corrects for
    bias (toward lower values) in the variance estimate introduced when the
    sample mean of `a` is used in place of the true mean of the population.
    The resulting estimate of the standard deviation is still biased, but less
    than it would have been without the correction. For this quantity, use
    ``ddof=1``.

    Note that, for complex numbers, `std` takes the absolute
    value before squaring, so that the result is always real and nonnegative.

    For floating-point input, the standard deviation is computed using the same
    precision the input has. Depending on the input data, this can cause
    the results to be inaccurate, especially for float32 (see example below).
    Specifying a higher-accuracy accumulator using the `dtype` keyword can
    alleviate this issue.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1, 2], [3, 4]])
    >>> np.std(a)
    1.1180339887498949 # may vary
    >>> np.std(a, axis=0)
    array([1.,  1.])
    >>> np.std(a, axis=1)
    array([0.5,  0.5])

    In single precision, std() can be inaccurate:

    >>> a = np.zeros((2, 512*512), dtype=np.float32)
    >>> a[0, :] = 1.0
    >>> a[1, :] = 0.1
    >>> np.std(a)
    np.float32(0.45000005)

    Computing the standard deviation in float64 is more accurate:

    >>> np.std(a, dtype=np.float64)
    0.44999999925494177 # may vary

    Specifying a where argument:

    >>> a = np.array([[14, 8, 11, 10], [7, 9, 10, 11], [10, 15, 5, 10]])
    >>> np.std(a)
    2.614064523559687 # may vary
    >>> np.std(a, where=[[True], [True], [False]])
    2.0

    Using the mean keyword to save computation time:

    >>> import numpy as np
    >>> from timeit import timeit
    >>> a = np.array([[14, 8, 11, 10], [7, 9, 10, 11], [10, 15, 5, 10]])
    >>> mean = np.mean(a, axis=1, keepdims=True)
    >>>
    >>> g = globals()
    >>> n = 10000
    >>> t1 = timeit("std = np.std(a, axis=1, mean=mean)", globals=g, number=n)
    >>> t2 = timeit("std = np.std(a, axis=1)", globals=g, number=n)
    >>> print(f'Percentage execution time saved {100*(t2-t1)/t2:.0f}%')
    #doctest: +SKIP
    Percentage execution time saved 30%

    """
    kwargs = {}
    if keepdims is not np._NoValue:
        kwargs['keepdims'] = keepdims
    if where is not np._NoValue:
        kwargs['where'] = where
    if mean is not np._NoValue:
        kwargs['mean'] = mean

    if correction != np._NoValue:
        if ddof != 0:
            raise ValueError(
                "ddof and correction can't be provided simultaneously."
            )
        else:
            ddof = correction

    if type(a) is not mu.ndarray:
        try:
            std = a.std
        except AttributeError:
            pass
        else:
            return std(axis=axis, dtype=dtype, out=out, ddof=ddof, **kwargs)

    return _methods._std(a, axis=axis, dtype=dtype, out=out, ddof=ddof,
                         **kwargs)


def std(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
        out: None = None, ddof: int = 0, keepdims: bool = False, *,
        where: ArrayLike | None = None, mean: ArrayLike | None = None,
        correction: int | float | None = None) -> Array:
  r"""Compute the standard deviation along a given axis.

  JAX implementation of :func:`numpy.std`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      standard deviation is computed. If None, standard deviaiton is computed
      along all the axes.
    dtype: The type of the output array. Default=None.
    ddof: int, default=0. Degrees of freedom. The divisor in the standard deviation
      computation is ``N-ddof``, ``N`` is number of elements along given axis.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    where: optional, boolean array, default=None. The elements to be used in the
      standard deviation. Array should be broadcast compatible to the input.
    mean: optional, mean of the input array, computed along the given axis.
      If provided, it will be used to compute the standard deviation instead of
      computing it from the input array. If specified, mean must be broadcast-compatible
      with the input array. In the general case, this can be achieved by computing the mean with
      ``keepdims=True`` and ``axis`` matching this function's ``axis`` argument.
    correction: int or float, default=None. Alternative name for ``ddof``.
      Both ddof and correction can't be provided simultaneously.
    out: Unused by JAX.

  Returns:
    An array of the standard deviation along the given axis.

  See also:
    - :func:`jax.numpy.var`: Compute the variance of array elements over given
      axis.
    - :func:`jax.numpy.mean`: Compute the mean of array elements over a given axis.
    - :func:`jax.numpy.nanvar`: Compute the variance along a given axis, ignoring
      NaNs values.
    - :func:`jax.numpy.nanstd`: Computed the standard deviation of a given axis,
      ignoring NaN values.

  Examples:
    By default, ``jnp.std`` computes the standard deviation along all axes.

    >>> x = jnp.array([[1, 3, 4, 2],
    ...                [4, 2, 5, 3],
    ...                [5, 4, 2, 3]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.std(x)
    Array(1.21, dtype=float32)

    If ``axis=0``, computes along axis 0.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.std(x, axis=0))
    [1.7  0.82 1.25 0.47]

    To preserve the dimensions of input, you can set ``keepdims=True``.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.std(x, axis=0, keepdims=True))
    [[1.7  0.82 1.25 0.47]]

    If ``ddof=1``:

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.std(x, axis=0, keepdims=True, ddof=1))
    [[2.08 1.   1.53 0.58]]

    To include specific elements of the array to compute standard deviation, you
    can use ``where``.

    >>> where = jnp.array([[1, 0, 1, 0],
    ...                    [0, 1, 0, 1],
    ...                    [1, 1, 1, 0]], dtype=bool)
    >>> jnp.std(x, axis=0, keepdims=True, where=where)
    Array([[2., 1., 1., 0.]], dtype=float32)
  """
  if correction is None:
    correction = ddof
  elif not isinstance(ddof, int) or ddof != 0:
    raise ValueError("ddof and correction can't be provided simultaneously.")
  a = ensure_arraylike("std", a)
  return _std(a, axis=_ensure_optional_axes(axis), dtype=dtype, out=out, correction=correction, keepdims=keepdims,
              where=where, mean=mean)

