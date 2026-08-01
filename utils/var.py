
def var(input: Tensor, unbiased: bool = True) -> Tensor:
    return var_decomposition(input, correction=(1 if unbiased else 0))


def var(
    input: Tensor | MaskedTensor,
    dim: DimOrDims = None,
    unbiased: bool | None = None,
    *,
    correction: int | float | None = None,
    keepdim: bool | None = False,
    dtype: DType | None = None,
    mask: Tensor | None = None,
) -> Tensor:
    """\
{reduction_signature}
{reduction_descr}
The identity value of sample variance operation is undefined. The
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
        take_sqrt=False,
    )


def var(
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
    result = tensor.var(dim=axis, correction=ddof)
    return _util.cast_if_needed(result, in_dtype)


def var(
    a: TensorLikeType,
    dim: DimsType | None = None,
    unbiased: bool | None = None,
    keepdim: bool = False,
    *,
    correction: NumberType | None = None,
) -> TensorLikeType:
    dim, unbiased = _dim_var_dispatch(dim, unbiased)
    correction = utils.set_correction(unbiased, correction)
    # reduces over all dimensions if dim=() is passed
    if dim == () or dim == []:
        dim = None

    result = _reduction(
        a,
        partial(prims.var, correction=correction),
        dims=dim,
        keepdims=keepdim,
        dtype=None,
        out=None,
        has_identity=True,
        output_dtype_kind=REDUCTION_OUTPUT_TYPE_KIND.COMPLEX_TO_FLOAT,
    )
    return result


def var(g: jit_utils.GraphContext, input, *args):
    var, _ = var_mean(g, input, *args)
    return var


def var():
    return lambda *args: Var(*args)


def var(names, **args):
    """
    Create symbols and inject them into the global namespace.

    Explanation
    ===========

    This calls :func:`symbols` with the same arguments and puts the results
    into the *global* namespace. It's recommended not to use :func:`var` in
    library code, where :func:`symbols` has to be used::

    Examples
    ========

    >>> from sympy import var

    >>> var('x')
    x
    >>> x # noqa: F821
    x

    >>> var('a,ab,abc')
    (a, ab, abc)
    >>> abc # noqa: F821
    abc

    >>> var('x,y', real=True)
    (x, y)
    >>> x.is_real and y.is_real # noqa: F821
    True

    See :func:`symbols` documentation for more details on what kinds of
    arguments can be passed to :func:`var`.

    """
    def traverse(symbols, frame):
        """Recursively inject symbols to the global namespace. """
        for symbol in symbols:
            if isinstance(symbol, Basic):
                frame.f_globals[symbol.name] = symbol
            elif isinstance(symbol, FunctionClass):
                frame.f_globals[symbol.__name__] = symbol
            else:
                traverse(symbol, frame)

    from inspect import currentframe
    frame = currentframe().f_back

    try:
        syms = symbols(names, **args)

        if syms is not None:
            if isinstance(syms, Basic):
                frame.f_globals[syms.name] = syms
            elif isinstance(syms, FunctionClass):
                frame.f_globals[syms.__name__] = syms
            else:
                traverse(syms, frame)
    finally:
        del frame  # break cyclic dependencies as stated in inspect docs

    return syms


def var(
    x: Array,
    /,
    xp: Namespace,
    *,
    axis: int | tuple[int, ...] | None = None,
    correction: float = 0.0,  # correction instead of ddof
    keepdims: bool = False,
    **kwargs: object,
) -> Array:
    return xp.var(x, axis=axis, ddof=correction, keepdims=keepdims, **kwargs)


def var(x: Array,
        /,
        *,
        axis: int | tuple[int, ...] | None = None,
        correction: float = 0.0,
        keepdims: bool = False,
        **kwargs: object) -> Array:
    # Note, float correction is not supported
    # https://github.com/pytorch/pytorch/issues/61492. We don't try to
    # implement it here for now.

    # if isinstance(correction, float):
    #     correction = int(correction)

    # https://github.com/pytorch/pytorch/issues/29137
    if axis == ():
        return torch.zeros_like(x)
    if isinstance(axis, int):
        axis = (axis,)
    if axis is None:
        # torch doesn't support keepdims with axis=None
        # (https://github.com/pytorch/pytorch/issues/71209)
        res = torch.var(x, tuple(range(x.ndim)), correction=correction, **kwargs)
        res = _axis_none_keepdims(res, x.ndim, keepdims)
        return res
    return torch.var(x, axis, correction=correction, keepdims=keepdims, **kwargs)


def var(
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
            np.var, values=values, mask=mask, skipna=skipna, axis=axis, ddof=ddof
        )


def var(a, axis=None, dtype=None, out=None, ddof=0, keepdims=np._NoValue, *,
        where=np._NoValue, mean=np._NoValue, correction=np._NoValue):
    r"""
    Compute the variance along the specified axis.

    Returns the variance of the array elements, a measure of the spread of a
    distribution.  The variance is computed for the flattened array by
    default, otherwise over the specified axis.

    Parameters
    ----------
    a : array_like
        Array containing numbers whose variance is desired.  If `a` is not an
        array, a conversion is attempted.
    axis : None or int or tuple of ints, optional
        Axis or axes along which the variance is computed.  The default is to
        compute the variance of the flattened array.
        If this is a tuple of ints, a variance is performed over multiple axes,
        instead of a single axis or all the axes as before.
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
        ``N - ddof``, where ``N`` represents the number of elements. By
        default `ddof` is zero. See notes for details about use of `ddof`.
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the input array.

        If the default value is passed, then `keepdims` will not be
        passed through to the `var` method of sub-classes of
        `ndarray`, however any non-default value will be.  If the
        sub-class' method does not implement `keepdims` any
        exceptions will be raised.
    where : array_like of bool, optional
        Elements to include in the variance. See `~numpy.ufunc.reduce` for
        details.

        .. versionadded:: 1.20.0

    mean : array like, optional
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
        If ``out=None``, returns a new array containing the variance;
        otherwise, a reference to the output array is returned.

    See Also
    --------
    std, mean, nanmean, nanstd, nanvar
    :ref:`ufuncs-output-type`

    Notes
    -----
    There are several common variants of the array variance calculation.
    Assuming the input `a` is a one-dimensional NumPy array and ``mean`` is
    either provided as an argument or computed as ``a.mean()``, NumPy
    computes the variance of an array as::

        N = len(a)
        d2 = abs(a - mean)**2  # abs is for complex `a`
        var = d2.sum() / (N - ddof)  # note use of `ddof`

    Different values of the argument `ddof` are useful in different
    contexts. NumPy's default ``ddof=0`` corresponds with the expression:

    .. math::

        \frac{\sum_i{|a_i - \bar{a}|^2 }}{N}

    which is sometimes called the "population variance" in the field of
    statistics because it applies the definition of variance to `a` as if `a`
    were a complete population of possible observations.

    Many other libraries define the variance of an array differently, e.g.:

    .. math::

        \frac{\sum_i{|a_i - \bar{a}|^2}}{N - 1}

    In statistics, the resulting quantity is sometimes called the "sample
    variance" because if `a` is a random sample from a larger population,
    this calculation provides an unbiased estimate of the variance of the
    population.  The use of :math:`N-1` in the denominator is often called
    "Bessel's correction" because it corrects for bias (toward lower values)
    in the variance estimate introduced when the sample mean of `a` is used
    in place of the true mean of the population. For this quantity, use
    ``ddof=1``.

    Note that for complex numbers, the absolute value is taken before
    squaring, so that the result is always real and nonnegative.

    For floating-point input, the variance is computed using the same
    precision the input has.  Depending on the input data, this can cause
    the results to be inaccurate, especially for `float32` (see example
    below).  Specifying a higher-accuracy accumulator using the ``dtype``
    keyword can alleviate this issue.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1, 2], [3, 4]])
    >>> np.var(a)
    1.25
    >>> np.var(a, axis=0)
    array([1.,  1.])
    >>> np.var(a, axis=1)
    array([0.25,  0.25])

    In single precision, var() can be inaccurate:

    >>> a = np.zeros((2, 512*512), dtype=np.float32)
    >>> a[0, :] = 1.0
    >>> a[1, :] = 0.1
    >>> np.var(a)
    np.float32(0.20250003)

    Computing the variance in float64 is more accurate:

    >>> np.var(a, dtype=np.float64)
    0.20249999932944759 # may vary
    >>> ((1-0.55)**2 + (0.1-0.55)**2)/2
    0.2025

    Specifying a where argument:

    >>> a = np.array([[14, 8, 11, 10], [7, 9, 10, 11], [10, 15, 5, 10]])
    >>> np.var(a)
    6.833333333333333 # may vary
    >>> np.var(a, where=[[True], [True], [False]])
    4.0

    Using the mean keyword to save computation time:

    >>> import numpy as np
    >>> from timeit import timeit
    >>>
    >>> a = np.array([[14, 8, 11, 10], [7, 9, 10, 11], [10, 15, 5, 10]])
    >>> mean = np.mean(a, axis=1, keepdims=True)
    >>>
    >>> g = globals()
    >>> n = 10000
    >>> t1 = timeit("var = np.var(a, axis=1, mean=mean)", globals=g, number=n)
    >>> t2 = timeit("var = np.var(a, axis=1)", globals=g, number=n)
    >>> print(f'Percentage execution time saved {100*(t2-t1)/t2:.0f}%')
    #doctest: +SKIP
    Percentage execution time saved 32%

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
            var = a.var

        except AttributeError:
            pass
        else:
            return var(axis=axis, dtype=dtype, out=out, ddof=ddof, **kwargs)

    return _methods._var(a, axis=axis, dtype=dtype, out=out, ddof=ddof,
                         **kwargs)


def var(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
        out: None = None, ddof: int = 0, keepdims: bool = False, *,
        where: ArrayLike | None = None, mean: ArrayLike | None = None,
        correction: int | float | None = None) -> Array:
  r"""Compute the variance along a given axis.

  JAX implementation of :func:`numpy.var`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      variance is computed. If None, variance is computed along all the axes.
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
    correction: int or float, default=None. Alternative name for ``ddof``.
      Both ddof and correction can't be provided simultaneously.
    out: Unused by JAX.

  Returns:
    An array of the variance along the given axis.

  See also:
    - :func:`jax.numpy.mean`: Compute the mean of array elements over a given axis.
    - :func:`jax.numpy.std`: Compute the standard deviation of array elements over
      given axis.
    - :func:`jax.numpy.nanvar`: Compute the variance along a given axis, ignoring
      NaNs values.
    - :func:`jax.numpy.nanstd`: Computed the standard deviation of a given axis,
      ignoring NaN values.

  Examples:
    By default, ``jnp.var`` computes the variance along all axes.

    >>> x = jnp.array([[1, 3, 4, 2],
    ...                [5, 2, 6, 3],
    ...                [8, 4, 2, 9]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.var(x)
    Array(5.74, dtype=float32)

    If ``axis=1``, variance is computed along axis 1.

    >>> jnp.var(x, axis=1)
    Array([1.25  , 2.5   , 8.1875], dtype=float32)

    To preserve the dimensions of input, you can set ``keepdims=True``.

    >>> jnp.var(x, axis=1, keepdims=True)
    Array([[1.25  ],
           [2.5   ],
           [8.1875]], dtype=float32)

    If ``ddof=1``:

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.var(x, axis=1, keepdims=True, ddof=1))
    [[ 1.67]
     [ 3.33]
     [10.92]]

    To include specific elements of the array to compute variance, you can use
    ``where``.

    >>> where = jnp.array([[1, 0, 1, 0],
    ...                    [0, 1, 1, 0],
    ...                    [1, 1, 1, 0]], dtype=bool)
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.var(x, axis=1, keepdims=True, where=where))
    [[2.25]
     [4.  ]
     [6.22]]
  """
  if correction is None:
    correction = ddof
  elif not isinstance(ddof, int) or ddof != 0:
    raise ValueError("ddof and correction can't be provided simultaneously.")
  a = ensure_arraylike("var", a)
  return _var(a, axis=_ensure_optional_axes(axis), dtype=dtype, out=out, correction=correction, keepdims=keepdims,
              where=where, a_mean=mean)

