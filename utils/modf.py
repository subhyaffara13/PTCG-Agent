
def modf(x, /, *args, **kwds):
    quot, rem = divmod(x, 1, *args, **kwds)
    return rem, quot


def modf(x: ArrayLike, /, out=None) -> tuple[Array, Array]:
  """Return element-wise fractional and integral parts of the input array.

  JAX implementation of :obj:`numpy.modf`.

  Args:
    x: input array or scalar.
    out: Not used by JAX.

  Returns:
    An array containing the fractional and integral parts of the elements of ``x``,
    promoting dtypes inexact.

  See also:
    - :func:`jax.numpy.divmod`: Calculates the integer quotient and remainder of
      ``x1`` by ``x2`` element-wise.

  Examples:
    >>> jnp.modf(4.8)
    (Array(0.8000002, dtype=float32, weak_type=True), Array(4., dtype=float32, weak_type=True))
    >>> x = jnp.array([-3.4, -5.7, 0.6, 1.5, 2.3])
    >>> jnp.modf(x)
    (Array([-0.4000001 , -0.6999998 ,  0.6       ,  0.5       ,  0.29999995],      dtype=float32), Array([-3., -5.,  0.,  1.,  2.], dtype=float32))
  """
  x = ensure_arraylike("modf", x)
  x, = promote_dtypes_inexact(x)
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.modf is not supported.")
  whole = _where(lax.ge(x, lax._zero(x)), floor(x), ceil(x))
  return x - whole, whole

