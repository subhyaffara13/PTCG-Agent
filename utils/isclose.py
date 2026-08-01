
def isclose(a: ArrayLike, b: ArrayLike, rtol=1.0e-5, atol=1.0e-8, equal_nan=False):
    dtype = _dtypes_impl.result_type_impl(a, b)
    a = _util.cast_if_needed(a, dtype)
    b = _util.cast_if_needed(b, dtype)
    return torch.isclose(a, b, rtol=rtol, atol=atol, equal_nan=equal_nan)


def isclose(
    a: TensorLikeType,
    b: TensorLikeType,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    equal_nan: bool = False,
) -> TensorLikeType:
    _check_close_args(name="torch.isclose", a=a, b=b, rtol=rtol, atol=atol)

    close = eq(a, b)
    if equal_nan and (utils.is_float_dtype(a.dtype) or utils.is_complex_dtype(a.dtype)):
        close = logical_or(close, logical_and(isnan(a), isnan(b)))

    # Note: In case of zero tolerances the closeness inequality degenerates to an equality check.
    # In this case, the short-circuit prevents false positives as detailed in the paragraph below.
    if atol == 0 and rtol == 0:
        return close

    # Note [closeness error computation]
    # atol and rtol are provided as doubles, so the computation
    # rtol * other will produce a float or complex tensor.
    # When the difference (self - other) is compared to it then the
    # tensor representing the difference will also be cast to float or complex.
    # However, since (self - other) in uint8 is very likely to produce a
    # negative value, this moves the cast forward so the difference is
    # always computed in a float or complex type.
    # If the values of the integer tensors cannot be exactly represented
    # by the default scalar type then this may cause an incorrect result.
    if not utils.is_float_dtype(a.dtype) and not utils.is_complex_dtype(a.dtype):
        a = prims.convert_element_type(a, torch.get_default_dtype())
        b = prims.convert_element_type(b, torch.get_default_dtype())

    allowed_error = add(atol, abs(mul(b, rtol)))
    actual_error = abs(sub(a, b))

    # Computes finite closeness
    result = logical_or(
        close, logical_and(isfinite(actual_error), le(actual_error, allowed_error))
    )

    return result


def isclose(a, b):
    rtol = 1e-5
    atol = 1e-8
    return abs(a-b) <= atol + rtol*abs(b)


def isclose(
    a: Array | complex,
    b: Array | complex,
    *,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    equal_nan: bool = False,
    xp: ModuleType | None = None,
) -> Array:
    """
    Return a boolean array where two arrays are element-wise equal within a tolerance.

    The tolerance values are positive, typically very small numbers. The relative
    difference ``(rtol * abs(b))`` and the absolute difference `atol` are added together
    to compare against the absolute difference between `a` and `b`.

    NaNs are treated as equal if they are in the same place and if ``equal_nan=True``.
    Infs are treated as equal if they are in the same place and of the same sign in both
    arrays.

    Parameters
    ----------
    a, b : Array | int | float | complex | bool
        Input objects to compare. At least one must be an array.
    rtol : array_like, optional
        The relative tolerance parameter (see Notes).
    atol : array_like, optional
        The absolute tolerance parameter (see Notes).
    equal_nan : bool, optional
        Whether to compare NaN's as equal. If True, NaN's in `a` will be considered
        equal to NaN's in `b` in the output array.
    xp : array_namespace, optional
        The standard-compatible namespace for `a` and `b`. Default: infer.

    Returns
    -------
    Array
        A boolean array of shape broadcasted from `a` and `b`, containing ``True`` where
        `a` is close to `b`, and ``False`` otherwise.

    Warnings
    --------
    The default `atol` is not appropriate for comparing numbers with magnitudes much
    smaller than one (see notes).

    See Also
    --------
    math.isclose : Similar function in stdlib for Python scalars.

    Notes
    -----
    For finite values, `isclose` uses the following equation to test whether two
    floating point values are equivalent::

        absolute(a - b) <= (atol + rtol * absolute(b))

    Unlike the built-in `math.isclose`,
    the above equation is not symmetric in `a` and `b`,
    so that ``isclose(a, b)`` might be different from ``isclose(b, a)`` in some rare
    cases.

    The default value of `atol` is not appropriate when the reference value `b` has
    magnitude smaller than one. For example, it is unlikely that ``a = 1e-9`` and
    ``b = 2e-9`` should be considered "close", yet ``isclose(1e-9, 2e-9)`` is ``True``
    with default settings. Be sure to select `atol` for the use case at hand, especially
    for defining the threshold below which a non-zero value in `a` will be considered
    "close" to a very small or zero value in `b`.

    The comparison of `a` and `b` uses standard broadcasting, which means that `a` and
    `b` need not have the same shape in order for ``isclose(a, b)`` to evaluate to
    ``True``.

    `isclose` is not defined for non-numeric data types.
    ``bool`` is considered a numeric data-type for this purpose.
    """
    xp = array_namespace(a, b) if xp is None else xp

    if (
        is_numpy_namespace(xp)
        or is_cupy_namespace(xp)
        or is_dask_namespace(xp)
        or is_jax_namespace(xp)
    ):
        return xp.isclose(a, b, rtol=rtol, atol=atol, equal_nan=equal_nan)

    if is_torch_namespace(xp):
        a, b = asarrays(a, b, xp=xp)  # Array API 2024.12 support
        return xp.isclose(a, b, rtol=rtol, atol=atol, equal_nan=equal_nan)

    return _funcs.isclose(a, b, rtol=rtol, atol=atol, equal_nan=equal_nan, xp=xp)


def isclose(
    a: Array | complex,
    b: Array | complex,
    *,
    rtol: float = 1e-05,
    atol: float = 1e-08,
    equal_nan: bool = False,
    xp: ModuleType,
) -> Array:  # numpydoc ignore=PR01,RT01
    """See docstring in array_api_extra._delegation."""
    a, b = asarrays(a, b, xp=xp)

    a_inexact = xp.isdtype(a.dtype, ("real floating", "complex floating"))
    b_inexact = xp.isdtype(b.dtype, ("real floating", "complex floating"))
    if a_inexact or b_inexact:
        # prevent warnings on NumPy and Dask on inf - inf
        mxp = meta_namespace(a, b, xp=xp)
        out = apply_where(
            xp.isinf(a) | xp.isinf(b),
            (a, b),
            lambda a, b: mxp.isinf(a) & mxp.isinf(b) & (mxp.sign(a) == mxp.sign(b)),  # pyright: ignore[reportUnknownArgumentType]
            # Note: inf <= inf is True!
            lambda a, b: mxp.abs(a - b) <= (atol + rtol * mxp.abs(b)),  # pyright: ignore[reportUnknownArgumentType]
            xp=xp,
        )
        if equal_nan:
            out = xp.where(xp.isnan(a) & xp.isnan(b), True, out)
        return out

    if xp.isdtype(a.dtype, "bool") or xp.isdtype(b.dtype, "bool"):
        if atol >= 1 or rtol >= 1:
            return xp.ones_like(a == b)
        return a == b

    # integer types
    atol = int(atol)
    if rtol == 0:
        return xp.abs(a - b) <= atol

    # Don't rely on OverflowError, as it is not guaranteed by the Array API.
    nrtol = int(1.0 / rtol)
    if nrtol > xp.iinfo(b.dtype).max:
        # rtol * max_int < 1, so it's inconsequential
        return xp.abs(a - b) <= atol
    return xp.abs(a - b) <= (atol + xp.abs(b) // nrtol)


def isclose(a, b, rtol=1.e-5, atol=1.e-8, equal_nan=False):
    """
    Returns a boolean array where two arrays are element-wise equal within a
    tolerance.

    The tolerance values are positive, typically very small numbers.  The
    relative difference (`rtol` * abs(`b`)) and the absolute difference
    `atol` are added together to compare against the absolute difference
    between `a` and `b`.

    .. warning:: The default `atol` is not appropriate for comparing numbers
                 with magnitudes much smaller than one (see Notes).

    Parameters
    ----------
    a, b : array_like
        Input arrays to compare.
    rtol : array_like
        The relative tolerance parameter (see Notes).
    atol : array_like
        The absolute tolerance parameter (see Notes).
    equal_nan : bool
        Whether to compare NaN's as equal.  If True, NaN's in `a` will be
        considered equal to NaN's in `b` in the output array.

    Returns
    -------
    y : array_like
        Returns a boolean array of where `a` and `b` are equal within the
        given tolerance. If both `a` and `b` are scalars, returns a single
        boolean value.

    See Also
    --------
    allclose
    math.isclose

    Notes
    -----
    For finite values, isclose uses the following equation to test whether
    two floating point values are equivalent.::

     absolute(a - b) <= (atol + rtol * absolute(b))

    Unlike the built-in `math.isclose`, the above equation is not symmetric
    in `a` and `b` -- it assumes `b` is the reference value -- so that
    `isclose(a, b)` might be different from `isclose(b, a)`.

    The default value of `atol` is not appropriate when the reference value
    `b` has magnitude smaller than one. For example, it is unlikely that
    ``a = 1e-9`` and ``b = 2e-9`` should be considered "close", yet
    ``isclose(1e-9, 2e-9)`` is ``True`` with default settings. Be sure
    to select `atol` for the use case at hand, especially for defining the
    threshold below which a non-zero value in `a` will be considered "close"
    to a very small or zero value in `b`.

    `isclose` is not defined for non-numeric data types.
    :class:`bool` is considered a numeric data-type for this purpose.

    Examples
    --------
    >>> import numpy as np
    >>> np.isclose([1e10,1e-7], [1.00001e10,1e-8])
    array([ True, False])

    >>> np.isclose([1e10,1e-8], [1.00001e10,1e-9])
    array([ True, True])

    >>> np.isclose([1e10,1e-8], [1.0001e10,1e-9])
    array([False,  True])

    >>> np.isclose([1.0, np.nan], [1.0, np.nan])
    array([ True, False])

    >>> np.isclose([1.0, np.nan], [1.0, np.nan], equal_nan=True)
    array([ True, True])

    >>> np.isclose([1e-8, 1e-7], [0.0, 0.0])
    array([ True, False])

    >>> np.isclose([1e-100, 1e-7], [0.0, 0.0], atol=0.0)
    array([False, False])

    >>> np.isclose([1e-10, 1e-10], [1e-20, 0.0])
    array([ True,  True])

    >>> np.isclose([1e-10, 1e-10], [1e-20, 0.999999e-10], atol=0.0)
    array([False,  True])

    """
    # Turn all but python scalars into arrays.
    x, y, atol, rtol = (
        a if isinstance(a, (int, float, complex)) else asanyarray(a)
        for a in (a, b, atol, rtol))

    # Make sure y is an inexact type to avoid bad behavior on abs(MIN_INT).
    # This will cause casting of x later. Also, make sure to allow subclasses
    # (e.g., for numpy.ma).
    # NOTE: We explicitly allow timedelta, which used to work. This could
    #       possibly be deprecated. See also gh-18286.
    #       timedelta works if `atol` is an integer or also a timedelta.
    #       Although, the default tolerances are unlikely to be useful
    if (dtype := getattr(y, "dtype", None)) is not None and dtype.kind != "m":
        dt = multiarray.result_type(y, 1.)
        y = asanyarray(y, dtype=dt)
    elif isinstance(y, int):
        y = float(y)

    # atol and rtol can be arrays
    if not (np.all(np.isfinite(atol)) and np.all(np.isfinite(rtol))):
        err_s = np.geterr()["invalid"]
        err_msg = f"One of rtol or atol is not valid, atol: {atol}, rtol: {rtol}"

        if err_s == "warn":
            warnings.warn(err_msg, RuntimeWarning, stacklevel=2)
        elif err_s == "raise":
            raise FloatingPointError(err_msg)
        elif err_s == "print":
            print(err_msg)

    with errstate(invalid='ignore'):

        result = (less_equal(abs(x - y), atol + rtol * abs(y))
                  & isfinite(y)
                  | (x == y))
        if equal_nan:
            result |= isnan(x) & isnan(y)

    return result[()]  # Flatten 0d arrays to scalars


def isclose(a: ArrayLike, b: ArrayLike, rtol: ArrayLike = 1e-05, atol: ArrayLike = 1e-08,
            equal_nan: bool = False) -> Array:
  r"""Check if the elements of two arrays are approximately equal within a tolerance.

  JAX implementation of :func:`numpy.allclose`.

  Essentially this function evaluates the following condition:

  .. math::

     |a - b| \le \mathtt{atol} + \mathtt{rtol} * |b|

  ``jnp.inf`` in ``a`` will be considered equal to ``jnp.inf`` in ``b``.

  Args:
    a: first input array to compare.
    b: second input array to compare.
    rtol: relative tolerance used for approximate equality. Default = 1e-05.
    atol: absolute tolerance used for approximate equality. Default = 1e-08.
    equal_nan: Boolean. If ``True``, NaNs in ``a`` will be considered
      equal to NaNs in ``b``. Default is ``False``.

  Returns:
    A new array containing boolean values indicating whether the input arrays
    are element-wise approximately equal within the specified tolerances.

  See Also:
    - :func:`jax.numpy.allclose`
    - :func:`jax.numpy.equal`

  Examples:
    >>> jnp.isclose(jnp.array([1e6, 2e6, jnp.inf]), jnp.array([1e6, 2e7, jnp.inf]))
    Array([ True, False,  True], dtype=bool)
    >>> jnp.isclose(jnp.array([1e6, 2e6, 3e6]),
    ...              jnp.array([1.00008e6, 2.00008e7, 3.00008e8]), rtol=1e3)
    Array([ True,  True,  True], dtype=bool)
    >>> jnp.isclose(jnp.array([1e6, 2e6, 3e6]),
    ...              jnp.array([1.00001e6, 2.00002e6, 3.00009e6]), atol=1e3)
    Array([ True,  True,  True], dtype=bool)
    >>> jnp.isclose(jnp.array([jnp.nan, 1, 2]),
    ...              jnp.array([jnp.nan, 1, 2]), equal_nan=True)
    Array([ True,  True,  True], dtype=bool)
  """
  a, b = util.promote_args("isclose", a, b)
  dtype = a.dtype
  if dtypes.issubdtype(dtype, dtypes.extended):
    return lax.eq(a, b)

  a, b = util.promote_args_inexact("isclose", a, b)
  dtype = a.dtype
  if issubdtype(dtype, np.complexfloating):
    dtype = np.array(0, dtype).real.dtype
  rtol = lax.convert_element_type(rtol, dtype)
  atol = lax.convert_element_type(atol, dtype)
  both_nan = ufuncs.logical_and(ufuncs.isnan(a), ufuncs.isnan(b))
  check_fin = ufuncs.isfinite(b)
  in_range = lax.le(
    lax.abs(lax.sub(a, b)),
    lax.add(atol, lax.mul(rtol, lax.abs(b))))
  out = ufuncs.logical_or(lax.eq(a, b), ufuncs.logical_and(check_fin, in_range))
  return ufuncs.logical_or(out, both_nan) if equal_nan else out

