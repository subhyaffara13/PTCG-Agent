
def round(x):
    if is_integer_type(x):
        return clone(x)
    else:
        fn = ops_wrapper("round")
        return make_pointwise(fn)(x)


def round(a: ArrayLike, decimals=0, out: OutArray | None = None):
    if a.is_floating_point():
        result = torch.round(a, decimals=decimals)
    elif a.is_complex():
        # RuntimeError: "round_cpu" not implemented for 'ComplexFloat'
        result = torch.complex(
            torch.round(a.real, decimals=decimals),
            torch.round(a.imag, decimals=decimals),
        )
    else:
        # RuntimeError: "round_cpu" not implemented for 'int'
        result = a
    return result


def round(a: TensorLikeType, *, decimals: int = 0) -> TensorLikeType:
    if decimals == 0:
        return prims.round(a)
    else:
        ten_pow = 10**decimals
        ten_neg_pow = 10 ** (-decimals)
        return prims.mul(prims.round(prims.mul(a, ten_pow)), ten_neg_pow)


def round(g: jit_utils.GraphContext, self, decimals=0):
    if not symbolic_helper._is_fp(self):
        return self
    if decimals == 0:
        return g.op("Round", self)
    mul = g.op("Mul", self, g.op("Constant", value_t=torch.tensor(pow(10, decimals))))
    round = g.op("Round", mul)
    return g.op(
        "Mul", round, g.op("Constant", value_t=torch.tensor(pow(10, -1 * decimals)))
    )


def round(a, decimals=0, out=None):
    """
    Return a copy of a, rounded to 'decimals' places.

    When 'decimals' is negative, it specifies the number of positions
    to the left of the decimal point.  The real and imaginary parts of
    complex numbers are rounded separately. Nothing is done if the
    array is not of float type and 'decimals' is greater than or equal
    to 0.

    Parameters
    ----------
    decimals : int
        Number of decimals to round to. May be negative.
    out : array_like
        Existing array to use for output.
        If not given, returns a default copy of a.

    Notes
    -----
    If out is given and does not have a mask attribute, the mask of a
    is lost!

    Examples
    --------
    >>> import numpy as np
    >>> import numpy.ma as ma
    >>> x = [11.2, -3.973, 0.801, -1.41]
    >>> mask = [0, 0, 0, 1]
    >>> masked_x = ma.masked_array(x, mask)
    >>> masked_x
    masked_array(data=[11.2, -3.973, 0.801, --],
                 mask=[False, False, False, True],
        fill_value=1e+20)
    >>> ma.round(masked_x)
    masked_array(data=[11.0, -4.0, 1.0, --],
                 mask=[False, False, False, True],
        fill_value=1e+20)
    >>> ma.round(masked_x, decimals=1)
    masked_array(data=[11.2, -4.0, 0.8, --],
                 mask=[False, False, False, True],
        fill_value=1e+20)
    >>> ma.round(masked_x, decimals=-1)
    masked_array(data=[10.0, -0.0, 0.0, --],
                 mask=[False, False, False, True],
        fill_value=1e+20)
    """
    if out is None:
        return np.round(a, decimals, out)
    else:
        np.round(getdata(a), decimals, out)
        if hasattr(out, '_mask'):
            out._mask = getmask(a)
        return out


def round(a, decimals=0, out=None):
    """
    Evenly round to the given number of decimals.

    Parameters
    ----------
    a : array_like
        Input data.
    decimals : int, optional
        Number of decimal places to round to (default: 0).  If
        decimals is negative, it specifies the number of positions to
        the left of the decimal point.
    out : ndarray, optional
        Alternative output array in which to place the result. It must have
        the same shape as the expected output, but the type of the output
        values will be cast if necessary. See :ref:`ufuncs-output-type`
        for more details.

    Returns
    -------
    rounded_array : ndarray
        An array of the same type as `a`, containing the rounded values.
        Unless `out` was specified, a new array is created.  A reference to
        the result is returned.

        The real and imaginary parts of complex numbers are rounded
        separately.  The result of rounding a float is a float.

    See Also
    --------
    ndarray.round : equivalent method
    around : an alias for this function
    ceil, fix, floor, rint, trunc


    Notes
    -----
    For values exactly halfway between rounded decimal values, NumPy
    rounds to the nearest even value. Thus 1.5 and 2.5 round to 2.0,
    -0.5 and 0.5 round to 0.0, etc.

    ``np.round`` uses a fast but sometimes inexact algorithm to round
    floating-point datatypes. For positive `decimals` it is equivalent to
    ``np.true_divide(np.rint(a * 10**decimals), 10**decimals)``, which has
    error due to the inexact representation of decimal fractions in the IEEE
    floating point standard [1]_ and errors introduced when scaling by powers
    of ten. For instance, note the extra "1" in the following:

        >>> np.round(56294995342131.5, 3)
        56294995342131.51

    If your goal is to print such values with a fixed number of decimals, it is
    preferable to use numpy's float printing routines to limit the number of
    printed decimals:

        >>> np.format_float_positional(56294995342131.5, precision=3)
        '56294995342131.5'

    The float printing routines use an accurate but much more computationally
    demanding algorithm to compute the number of digits after the decimal
    point.

    Alternatively, Python's builtin `round` function uses a more accurate
    but slower algorithm for 64-bit floating point values:

        >>> round(56294995342131.5, 3)
        56294995342131.5
        >>> np.round(16.055, 2), round(16.055, 2)  # equals 16.0549999999999997
        (16.06, 16.05)


    References
    ----------
    .. [1] "Lecture Notes on the Status of IEEE 754", William Kahan,
           https://people.eecs.berkeley.edu/~wkahan/ieee754status/IEEE754.PDF

    Examples
    --------
    >>> import numpy as np
    >>> np.round([0.37, 1.64])
    array([0., 2.])
    >>> np.round([0.37, 1.64], decimals=1)
    array([0.4, 1.6])
    >>> np.round([.5, 1.5, 2.5, 3.5, 4.5]) # rounds to nearest even value
    array([0., 2., 2., 4., 4.])
    >>> np.round([1,2,3,11], decimals=1) # ndarray of ints is returned
    array([ 1,  2,  3, 11])
    >>> np.round([1,2,3,11], decimals=-1)
    array([ 0,  0,  0, 10])

    """
    return _wrapfunc(a, 'round', decimals=decimals, out=out)


def round(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return RoundOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def round(x):
  return np.trunc(
    x + np.copysign(np.nextafter(np.array(.5, dtype=x.dtype),
                                 np.array(0., dtype=x.dtype),
                                 dtype=x.dtype), x)).astype(x.dtype)


def round(x: ArrayLike,
          rounding_method: RoundingMethod = RoundingMethod.AWAY_FROM_ZERO
          ) -> Array:
  r"""Elementwise round.

  Rounds values to the nearest integer. This function lowers directly to the
  `stablehlo.round`_ operation.

  Args:
    x: an array or scalar value to round. Must have floating-point type.
    rounding_method: the method to use when rounding halfway values
      (e.g., ``0.5``). See :class:`jax.lax.RoundingMethod` for possible values.

  Returns:
    An array of the same shape and dtype as ``x``, containing the elementwise
    rounding of ``x``.

  See also:
    - :func:`jax.lax.floor`: round to the next integer toward negative infinity
    - :func:`jax.lax.ceil`: round to the next integer toward positive infinity

  Examples:
    >>> import jax.numpy as jnp
    >>> from jax import lax
    >>> x = jnp.array([-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5])
    >>> jax.lax.round(x)  # defaults method is AWAY_FROM_ZERO
    Array([-2., -1., -1.,  0.,  1.,  1.,  2.], dtype=float32)
    >>> jax.lax.round(x, rounding_method=jax.lax.RoundingMethod.TO_NEAREST_EVEN)
    Array([-2., -1., -0.,  0.,  0.,  1.,  2.], dtype=float32)

  .. _stablehlo.round: https://openxla.org/stablehlo/spec#round
  """
  rounding_method = RoundingMethod(rounding_method)
  return round_p.bind(x, rounding_method=rounding_method)


def round(a: ArrayLike, decimals: int = 0, out: None = None) -> Array:
  """Round input evenly to the given number of decimals.

  JAX implementation of :func:`numpy.round`.

  Args:
    a: input array or scalar.
    decimals: int, default=0. Number of decimal points to which the input needs
      to be rounded. It must be specified statically. Not implemented for
      ``decimals < 0``.
    out: Unused by JAX.

  Returns:
    An array containing the rounded values to the specified ``decimals`` with
    same shape and dtype as ``a``.

  Note:
    ``jnp.round`` rounds to the nearest even integer for the values exactly halfway
    between rounded decimal values.

  See also:
    - :func:`jax.numpy.floor`: Rounds the input to the nearest integer downwards.
    - :func:`jax.numpy.ceil`: Rounds the input to the nearest integer upwards.
    - :func:`jax.numpy.fix` and :func:numpy.trunc`: Rounds the input to the
      nearest integer towards zero.

  Examples:
    >>> x = jnp.array([1.532, 3.267, 6.149])
    >>> jnp.round(x)
    Array([2., 3., 6.], dtype=float32)
    >>> jnp.round(x, decimals=2)
    Array([1.53, 3.27, 6.15], dtype=float32)

    For values exactly halfway between rounded values:

    >>> x1 = jnp.array([10.5, 21.5, 12.5, 31.5])
    >>> jnp.round(x1)
    Array([10., 22., 12., 32.], dtype=float32)
  """
  a = util.ensure_arraylike("round", a)
  decimals = core.concrete_or_error(operator.index, decimals, "'decimals' argument of jnp.round")
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.round is not supported.")
  dtype = a.dtype
  if issubdtype(dtype, np.integer):
    if decimals < 0:
      raise NotImplementedError(
        "integer np.round not implemented for decimals < 0")
    return a  # no-op on integer types

  def _round_float(x: ArrayLike) -> Array:
    if decimals == 0:
      return lax.round(x, lax.RoundingMethod.TO_NEAREST_EVEN)

    # TODO(phawkins): the strategy of rescaling the value isn't necessarily a
    # good one since we may be left with an incorrectly rounded value at the
    # end due to precision problems. As a workaround for float16, convert to
    # float32,
    x = lax.convert_element_type(x, np.float32) if dtype == np.float16 else x
    factor = lax._const(x, 10 ** decimals)
    out = lax.div(lax.round(lax.mul(x, factor),
                            lax.RoundingMethod.TO_NEAREST_EVEN), factor)
    return lax.convert_element_type(out, dtype) if dtype == np.float16 else out

  if decimals > np.log10(dtypes.finfo(dtype).max):
    # Rounding beyond the input precision is a no-op.
    return lax.asarray(a)
  if issubdtype(dtype, np.complexfloating):
    return lax.complex(_round_float(lax.real(a)), _round_float(lax.imag(a)))
  else:
    return _round_float(a)


def round(x: FloatArray['*d']) -> FloatArray['*d']:  # pylint: disable=redefined-builtin
  """`x.round()` for jnp, tnp, np, otrch."""
  if lazy.is_tf(x):  # TODO(b/219427516): missing method
    return lazy.tnp.around(x)
  return x.round()

