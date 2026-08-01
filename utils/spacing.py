
def spacing(x: ArrayLike, /) -> Array:
  """Return the spacing between ``x`` and the next adjacent number.

  JAX implementation of :func:`numpy.spacing`.

  Args:
    x: real-valued array. Integer or boolean types will be cast to float.

  Returns:
    Array of same shape as ``x`` containing spacing between each entry of
    ``x`` and its closest adjacent value.

  See also:
    - :func:`jax.numpy.nextafter`: find the next representable value.

  Examples:
    >>> x = jnp.array([0.0, 0.25, 0.5, 0.75, 1.0], dtype='float32')
    >>> jnp.spacing(x)
    Array([1.4012985e-45, 2.9802322e-08, 5.9604645e-08, 5.9604645e-08,
          1.1920929e-07], dtype=float32)

    For ``x = 1``, the spacing is equal to the ``eps`` value given by
    :class:`jax.numpy.finfo`:

    >>> x = jnp.float32(1)
    >>> jnp.spacing(x) == jnp.finfo(x.dtype).eps
    Array(True, dtype=bool)
  """
  arr, = promote_args_inexact("spacing", x)
  if dtypes.isdtype(arr.dtype, "complex floating"):
    raise ValueError("jnp.spacing is not defined for complex inputs.")
  inf = _lax_const(arr, np.inf)
  smallest_subnormal = dtypes.finfo(arr.dtype).smallest_subnormal

  # Numpy's behavior seems to depend on dtype
  if arr.dtype == 'float16':
    return lax.nextafter(arr, inf) - arr
  else:
    result = lax.nextafter(arr, copysign(inf, arr)) - arr
    return _where(result == 0, copysign(smallest_subnormal, arr), result)

