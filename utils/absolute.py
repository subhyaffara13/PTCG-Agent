
def absolute(x):
    # work around torch.absolute not impl for bools
    if x.dtype == torch.bool:
        return x
    return torch.absolute(x)


def absolute(x: ArrayLike, /) -> Array:
  r"""Calculate the absolute value element-wise.

  JAX implementation of :obj:`numpy.absolute`.

  This is the same function as :func:`jax.numpy.abs`.

  Args:
    x: Input array

  Returns:
    An array-like object containing the absolute value of each element in ``x``,
    with the same shape as ``x``. For complex valued input, :math:`a + ib`,
    the absolute value is :math:`\sqrt{a^2+b^2}`.

  Note:
    For complex inputs containing ``NaN`` in the real or imaginary part,
    ``abs`` will always return ``NaN``.

  Examples:
    >>> x1 = jnp.array([5, -2, 0, 12])
    >>> jnp.absolute(x1)
    Array([ 5,  2,  0, 12], dtype=int32)

    >>> x2 = jnp.array([[ 8, -3, 1],[ 0, 9, -6]])
    >>> jnp.absolute(x2)
    Array([[8, 3, 1],
           [0, 9, 6]], dtype=int32)

    >>> x3 = jnp.array([8 + 15j, 3 - 4j, -5 + 0j])
    >>> jnp.absolute(x3)
    Array([17.,  5.,  5.], dtype=float32)
  """
  x = ensure_arraylike('absolute', x)
  dt = x.dtype
  return lax.asarray(x) if dt == np.bool_ or dtypes.issubdtype(dt, np.unsignedinteger) else lax.abs(x)

