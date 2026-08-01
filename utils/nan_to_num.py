
def nan_to_num(self, nan=None, posinf=None, neginf=None):
    return torch.empty_like(self)


def nan_to_num(
    x: ArrayLike, copy: NotImplementedType = True, nan=0.0, posinf=None, neginf=None
):
    # work around RuntimeError: "nan_to_num" not implemented for 'ComplexDouble'
    if x.is_complex():
        re = torch.nan_to_num(x.real, nan=nan, posinf=posinf, neginf=neginf)
        im = torch.nan_to_num(x.imag, nan=nan, posinf=posinf, neginf=neginf)
        return re + 1j * im
    else:
        return torch.nan_to_num(x, nan=nan, posinf=posinf, neginf=neginf)


def nan_to_num(
    a: TensorLikeType,
    nan: NumberType | None = 0.0,
    posinf: NumberType | None = None,
    neginf: NumberType | None = None,
) -> TensorLikeType:
    if not isinstance(a, TensorLike):
        raise AssertionError(f"a must be TensorLike, got {type(a)}")

    if utils.is_boolean_dtype(a.dtype) or utils.is_integer_dtype(a.dtype):
        return a.clone()

    if nan is None:
        nan = 0.0

    if posinf is None:
        posinf = torch.finfo(a.dtype).max

    if neginf is None:
        neginf = torch.finfo(a.dtype).min

    result = torch.where(torch.isnan(a), nan, a)  # type: ignore[call-overload]
    result = torch.where(torch.isneginf(a), neginf, result)  # type: ignore[call-overload]
    result = torch.where(torch.isposinf(a), posinf, result)  # type: ignore[call-overload]
    return result


def nan_to_num(g: jit_utils.GraphContext, input, nan, posinf, neginf):
    # Cannot create a int type tensor with inf/nan values, so we simply
    # return the original tensor
    if not symbolic_helper._is_fp(input):
        return input
    input_dtype = _type_utils.JitScalarType.from_value(input).dtype()
    if nan is None:
        nan = 0.0
    nan_cond = opset9.isnan(g, input)
    nan_result = g.op(
        "Where",
        nan_cond,
        g.op("Constant", value_t=torch.tensor([nan], dtype=input_dtype)),
        input,
    )

    # For None values of posinf, neginf we use the greatest/lowest finite
    # value representable by input's dtype.
    finfo = torch.finfo(input_dtype)
    if posinf is None:
        posinf = finfo.max
    posinf_cond = opset9.logical_and(
        g,
        isinf(g, nan_result),
        opset9.gt(g, nan_result, g.op("Constant", value_t=torch.LongTensor([0]))),
    )
    nan_posinf_result = g.op(
        "Where",
        posinf_cond,
        g.op("Constant", value_t=torch.tensor([posinf], dtype=input_dtype)),
        nan_result,
    )

    if neginf is None:
        neginf = finfo.min
    neginf_cond = opset9.logical_and(
        g,
        isinf(g, nan_posinf_result),
        opset9.lt(
            g, nan_posinf_result, g.op("Constant", value_t=torch.LongTensor([0]))
        ),
    )
    return g.op(
        "Where",
        neginf_cond,
        g.op("Constant", value_t=torch.tensor([neginf], dtype=input_dtype)),
        nan_posinf_result,
    )


def nan_to_num(
    x: Array | float | complex,
    /,
    *,
    fill_value: int | float = 0.0,
    xp: ModuleType | None = None,
) -> Array:
    """
    Replace NaN with zero and infinity with large finite numbers (default behaviour).

    If `x` is inexact, NaN is replaced by zero or by the user defined value in the
    `fill_value` keyword, infinity is replaced by the largest finite floating
    point value representable by ``x.dtype``, and -infinity is replaced by the
    most negative finite floating point value representable by ``x.dtype``.

    For complex dtypes, the above is applied to each of the real and
    imaginary components of `x` separately.

    Parameters
    ----------
    x : array | float | complex
        Input data.
    fill_value : int | float, optional
        Value to be used to fill NaN values. If no value is passed
        then NaN values will be replaced with 0.0.
    xp : array_namespace, optional
        The standard-compatible namespace for `x`. Default: infer.

    Returns
    -------
    array
        `x`, with the non-finite values replaced.

    See Also
    --------
    array_api.isnan : Shows which elements are Not a Number (NaN).

    Examples
    --------
    >>> import array_api_extra as xpx
    >>> import array_api_strict as xp
    >>> xpx.nan_to_num(xp.inf)
    1.7976931348623157e+308
    >>> xpx.nan_to_num(-xp.inf)
    -1.7976931348623157e+308
    >>> xpx.nan_to_num(xp.nan)
    0.0
    >>> x = xp.asarray([xp.inf, -xp.inf, xp.nan, -128, 128])
    >>> xpx.nan_to_num(x)
    array([ 1.79769313e+308, -1.79769313e+308,  0.00000000e+000, # may vary
           -1.28000000e+002,  1.28000000e+002])
    >>> y = xp.asarray([complex(xp.inf, xp.nan), xp.nan, complex(xp.nan, xp.inf)])
    array([  1.79769313e+308,  -1.79769313e+308,   0.00000000e+000, # may vary
         -1.28000000e+002,   1.28000000e+002])
    >>> xpx.nan_to_num(y)
    array([  1.79769313e+308 +0.00000000e+000j, # may vary
             0.00000000e+000 +0.00000000e+000j,
             0.00000000e+000 +1.79769313e+308j])
    """
    if isinstance(fill_value, complex):
        msg = "Complex fill values are not supported."
        raise TypeError(msg)

    xp = array_namespace(x) if xp is None else xp

    # for scalars we want to output an array
    y = xp.asarray(x)

    if (
        is_cupy_namespace(xp)
        or is_jax_namespace(xp)
        or is_numpy_namespace(xp)
        or is_torch_namespace(xp)
    ):
        return xp.nan_to_num(y, nan=fill_value)

    return _funcs.nan_to_num(y, fill_value=fill_value, xp=xp)


def nan_to_num(  # numpydoc ignore=PR01,RT01
    x: Array,
    /,
    fill_value: int | float = 0.0,
    *,
    xp: ModuleType,
) -> Array:
    """See docstring in `array_api_extra._delegation.py`."""

    def perform_replacements(  # numpydoc ignore=PR01,RT01
        x: Array,
        fill_value: int | float,
        xp: ModuleType,
    ) -> Array:
        """Internal function to perform the replacements."""
        x = xp.where(xp.isnan(x), fill_value, x)

        # convert infinities to finite values
        finfo = xp.finfo(x.dtype)
        idx_posinf = xp.isinf(x) & ~xp.signbit(x)
        idx_neginf = xp.isinf(x) & xp.signbit(x)
        x = xp.where(idx_posinf, finfo.max, x)
        return xp.where(idx_neginf, finfo.min, x)

    if xp.isdtype(x.dtype, "complex floating"):
        return perform_replacements(
            xp.real(x),
            fill_value,
            xp,
        ) + 1j * perform_replacements(
            xp.imag(x),
            fill_value,
            xp,
        )

    if xp.isdtype(x.dtype, "numeric"):
        return perform_replacements(x, fill_value, xp)

    return x


def nan_to_num(x, copy=True, nan=0.0, posinf=None, neginf=None):
    """
    Replace NaN with zero and infinity with large finite numbers (default
    behaviour) or with the numbers defined by the user using the `nan`,
    `posinf` and/or `neginf` keywords.

    If `x` is inexact, NaN is replaced by zero or by the user defined value in
    `nan` keyword, infinity is replaced by the largest finite floating point
    values representable by ``x.dtype`` or by the user defined value in
    `posinf` keyword and -infinity is replaced by the most negative finite
    floating point values representable by ``x.dtype`` or by the user defined
    value in `neginf` keyword.

    For complex dtypes, the above is applied to each of the real and
    imaginary components of `x` separately.

    If `x` is not inexact, then no replacements are made.

    Parameters
    ----------
    x : scalar or array_like
        Input data.
    copy : bool, optional
        Whether to create a copy of `x` (True) or to replace values
        in-place (False). The in-place operation only occurs if
        casting to an array does not require a copy.
        Default is True.
    nan : int, float, or bool or array_like of int, float, or bool, optional
        Values to be used to fill NaN values. If no values are passed
        then NaN values will be replaced with 0.0.
    posinf : int, float, or bool or array_like of int, float, or bool, optional
        Values to be used to fill positive infinity values. If no values are
        passed then positive infinity values will be replaced with a very
        large number.
    neginf : int, float, or bool or array_like of int, float, or bool, optional
        Values to be used to fill negative infinity values. If no values are
        passed then negative infinity values will be replaced with a very
        small (or negative) number.

    Returns
    -------
    out : ndarray
        `x`, with the non-finite values replaced. If `copy` is False, this may
        be `x` itself.

    See Also
    --------
    isinf : Shows which elements are positive or negative infinity.
    isneginf : Shows which elements are negative infinity.
    isposinf : Shows which elements are positive infinity.
    isnan : Shows which elements are Not a Number (NaN).
    isfinite : Shows which elements are finite (not NaN, not infinity)

    Notes
    -----
    NumPy uses the IEEE Standard for Binary Floating-Point for Arithmetic
    (IEEE 754). This means that Not a Number is not equivalent to infinity.

    Examples
    --------
    >>> import numpy as np
    >>> np.nan_to_num(np.inf)
    1.7976931348623157e+308
    >>> np.nan_to_num(-np.inf)
    -1.7976931348623157e+308
    >>> np.nan_to_num(np.nan)
    0.0
    >>> x = np.array([np.inf, -np.inf, np.nan, -128, 128])
    >>> np.nan_to_num(x)
    array([ 1.79769313e+308, -1.79769313e+308,  0.00000000e+000, # may vary
           -1.28000000e+002,  1.28000000e+002])
    >>> np.nan_to_num(x, nan=-9999, posinf=33333333, neginf=33333333)
    array([ 3.3333333e+07,  3.3333333e+07, -9.9990000e+03,
           -1.2800000e+02,  1.2800000e+02])
    >>> nan = np.array([11, 12, -9999, 13, 14])
    >>> posinf = np.array([33333333, 11, 12, 13, 14])
    >>> neginf = np.array([11, 33333333, 12, 13, 14])
    >>> np.nan_to_num(x, nan=nan, posinf=posinf, neginf=neginf)
    array([ 3.3333333e+07,  3.3333333e+07, -9.9990000e+03, -1.2800000e+02,
            1.2800000e+02])
    >>> y = np.array([complex(np.inf, np.nan), np.nan, complex(np.nan, np.inf)])
    array([  1.79769313e+308,  -1.79769313e+308,   0.00000000e+000, # may vary
         -1.28000000e+002,   1.28000000e+002])
    >>> np.nan_to_num(y)
    array([  1.79769313e+308 +0.00000000e+000j, # may vary
             0.00000000e+000 +0.00000000e+000j,
             0.00000000e+000 +1.79769313e+308j])
    >>> np.nan_to_num(y, nan=111111, posinf=222222)
    array([222222.+111111.j, 111111.     +0.j, 111111.+222222.j])
    >>> nan = np.array([11, 12, 13])
    >>> posinf = np.array([21, 22, 23])
    >>> neginf = np.array([31, 32, 33])
    >>> np.nan_to_num(y, nan=nan, posinf=posinf, neginf=neginf)
    array([21.+11.j, 12. +0.j, 13.+23.j])
    """
    x = _nx.array(x, subok=True, copy=copy)
    xtype = x.dtype.type

    isscalar = (x.ndim == 0)

    if not issubclass(xtype, _nx.inexact):
        return x[()] if isscalar else x

    iscomplex = issubclass(xtype, _nx.complexfloating)

    dest = (x.real, x.imag) if iscomplex else (x,)
    maxf, minf = _getmaxmin(x.real.dtype)
    if posinf is not None:
        maxf = posinf
    if neginf is not None:
        minf = neginf
    for d in dest:
        idx_nan = isnan(d)
        idx_posinf = isposinf(d)
        idx_neginf = isneginf(d)
        _nx.copyto(d, nan, where=idx_nan)
        _nx.copyto(d, maxf, where=idx_posinf)
        _nx.copyto(d, minf, where=idx_neginf)
    return x[()] if isscalar else x


def nan_to_num(x: ArrayLike, copy: bool = True, nan: ArrayLike = 0.0,
               posinf: ArrayLike | None = None,
               neginf: ArrayLike | None = None) -> Array:
  """Replace NaN and infinite entries in an array.

  JAX implementation of :func:`numpy.nan_to_num`.

  Args:
    x: array of values to be replaced. If it does not have an inexact
       dtype it will be returned unmodified.
    copy: unused by JAX
    nan: value to substitute for NaN entries. Defaults to 0.0.
    posinf: value to substitute for positive infinite entries.
      Defaults to the maximum representable value.
    neginf: value to substitute for positive infinite entries.
      Defaults to the minimum representable value.

  Returns:
    A copy of ``x`` with the requested substitutions.

  See also:
    - :func:`jax.numpy.isnan`: return True where the array contains NaN
    - :func:`jax.numpy.isposinf`: return True where the array contains +inf
    - :func:`jax.numpy.isneginf`: return True where the array contains -inf

  Examples:
    >>> x = jnp.array([0, jnp.nan, 1, jnp.inf, 2, -jnp.inf])

    Default substitution values:

    >>> jnp.nan_to_num(x)
    Array([ 0.0000000e+00,  0.0000000e+00,  1.0000000e+00,  3.4028235e+38,
            2.0000000e+00, -3.4028235e+38], dtype=float32)

    Overriding substitutions for ``-inf`` and ``+inf``:

    >>> jnp.nan_to_num(x, posinf=999, neginf=-999)
    Array([   0.,    0.,    1.,  999.,    2., -999.], dtype=float32)

    If you only wish to substitute for NaN values while leaving ``inf`` values
    untouched, using :func:`~jax.numpy.where` with :func:`jax.numpy.isnan` is
    a better option:

    >>> jnp.where(jnp.isnan(x), 0, x)
    Array([  0.,   0.,   1.,  inf,   2., -inf], dtype=float32)
  """
  del copy
  x = util.ensure_arraylike("nan_to_num", x)
  dtype = x.dtype
  if not issubdtype(dtype, np.inexact):
    return x
  if issubdtype(dtype, np.complexfloating):
    return lax.complex(
      nan_to_num(lax.real(x), nan=nan, posinf=posinf, neginf=neginf),
      nan_to_num(lax.imag(x), nan=nan, posinf=posinf, neginf=neginf))
  info = finfo(dtype)
  posinf = info.max if posinf is None else posinf
  neginf = info.min if neginf is None else neginf
  out = where(ufuncs.isnan(x), asarray(nan, dtype=dtype), x)
  out = where(ufuncs.isposinf(out), asarray(posinf, dtype=dtype), out)
  out = where(ufuncs.isneginf(out), asarray(neginf, dtype=dtype), out)
  return out

