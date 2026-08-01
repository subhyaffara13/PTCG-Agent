
def signbit(a):
    return prims.signbit(a)


def signbit(x: ArrayLike, /) -> Array:
  """Return the sign bit of array elements.

  JAX implementation of :obj:`numpy.signbit`.

  Args:
    x: input array. Complex values are not supported.

  Returns:
    A boolean array of the same shape as ``x``, containing ``True``
    where the sign of ``x`` is negative, and ``False`` otherwise.

  See also:
    - :func:`jax.numpy.sign`: return the mathematical sign of array elements,
      i.e. ``-1``, ``0``, or ``+1``.

  Examples:
    :func:`signbit` on boolean values is always ``False``:

    >>> x = jnp.array([True, False])
    >>> jnp.signbit(x)
    Array([False, False], dtype=bool)

    :func:`signbit` on integer values is equivalent to ``x < 0``:

    >>> x = jnp.array([-2, -1, 0, 1, 2])
    >>> jnp.signbit(x)
    Array([ True,  True, False, False, False], dtype=bool)

    :func:`signbit` on floating point values returns the value of the actual
    sign bit from the float representation, including signed zero:

    >>> x = jnp.array([-1.5, -0.0, 0.0, 1.5])
    >>> jnp.signbit(x)
    Array([ True, True, False, False], dtype=bool)

    This also returns the sign bit for special values such as signed NaN
    and signed infinity:

    >>> x = jnp.array([jnp.nan, -jnp.nan, jnp.inf, -jnp.inf])
    >>> jnp.signbit(x)
    Array([False,  True, False,  True], dtype=bool)
    """
  x, = promote_args("signbit", x)
  dtype = x.dtype
  if dtypes.issubdtype(dtype, np.integer):
    return lax.lt(x, _constant_like(x, 0))
  elif dtypes.issubdtype(dtype, np.bool_):
    return lax.full_like(x, False, dtype=np.bool_)
  elif not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(
        "jax.numpy.signbit is not well defined for %s" % dtype)

  info = dtypes.finfo(dtype)
  if info.bits not in _INT_DTYPES:
    raise NotImplementedError(
        "jax.numpy.signbit only supports 16, 32, and 64-bit types.")
  int_type = _INT_DTYPES[info.bits]
  x = lax.bitcast_convert_type(x, int_type)
  return lax.convert_element_type(x >> (info.nexp + info.nmant), np.bool_)

