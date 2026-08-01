
def rint(x: ArrayLike, /) -> Array:
  """Rounds the elements of x to the nearest integer

  JAX implementation of :obj:`numpy.rint`.

  Args:
    x: Input array

  Returns:
    An array-like object containing the rounded elements of ``x``. Always promotes
    to inexact.

  Note:
    If an element of x is exactly half way, e.g. ``0.5`` or ``1.5``, rint will round
    to the nearest even integer.

  Examples:
    >>> x1 = jnp.array([5, 4, 7])
    >>> jnp.rint(x1)
    Array([5., 4., 7.], dtype=float32)

    >>> x2 = jnp.array([-2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5])
    >>> jnp.rint(x2)
    Array([-2., -2., -0.,  0.,  2.,  2.,  4.,  4.], dtype=float32)

    >>> x3 = jnp.array([-2.5+3.5j, 4.5-0.5j])
    >>> jnp.rint(x3)
    Array([-2.+4.j,  4.-0.j], dtype=complex64)
  """
  x = ensure_arraylike('rint', x)
  dtype = x.dtype
  if dtype == bool or dtypes.issubdtype(dtype, np.integer):
    return lax.convert_element_type(x, dtypes.default_float_dtype())
  if dtypes.issubdtype(dtype, np.complexfloating):
    return lax.complex(rint(lax.real(x)), rint(lax.imag(x)))
  return lax.round(x, lax.RoundingMethod.TO_NEAREST_EVEN)

