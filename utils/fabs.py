
def fabs(ctx, x):
    return abs(ctx.convert(x))


def fabs(x: ArrayLike, /) -> Array:
  """Compute the element-wise absolute values of the real-valued input.

  JAX implementation of :obj:`numpy.fabs`.

  Args:
    x: input array or scalar. Must not have a complex dtype.

  Returns:
    An array with same shape as ``x`` and dtype float, containing the element-wise
    absolute values.

  See also:
    - :func:`jax.numpy.absolute`: Computes the absolute values of the input including
      complex dtypes.
    - :func:`jax.numpy.abs`: Computes the absolute values of the input including
      complex dtypes.

  Examples:
    For integer inputs:

    >>> x = jnp.array([-5, -9, 1, 10, 15])
    >>> jnp.fabs(x)
    Array([ 5.,  9.,  1., 10., 15.], dtype=float32)

    For float type inputs:

    >>> x1 = jnp.array([-1.342, 5.649, 3.927])
    >>> jnp.fabs(x1)
    Array([1.342, 5.649, 3.927], dtype=float32)

    For boolean inputs:

    >>> x2 = jnp.array([True, False])
    >>> jnp.fabs(x2)
    Array([1., 0.], dtype=float32)
  """
  x = ensure_arraylike('fabs', x)
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    raise TypeError("ufunc 'fabs' does not support complex dtypes")
  return lax.abs(*promote_args_inexact('fabs', x))

