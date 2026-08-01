
def nextafter(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.nextafter(a, b)


def nextafter(x1: ArrayLike, x2: ArrayLike) -> Array:
  """Returns the next representable value after ``x1`` in the direction of ``x2``.

  This function lowers directly to the ``chlo.next_after`` operation.

  Args:
    x1, x2: input arrays. Must have a matching floating-point dtypes. If neither is
      a scalar, must have the same number of dimensions and be broadcast-compatible.

  Returns:
    Array of the same dtype and broadcasted shape of the inputs, containing the
    next representable floating-point value after ``x1`` in the direction of
    ``x2``.

  Notes:
    In some environments flush-denormal-to-zero semantics is used.
    This means that, around zero, this function returns strictly non-zero
    values which appear as zero in any operations. Consider this example::

      >>> from jax import lax
      >>> lax.nextafter(0.0, 1.0)  # denormal numbers are representable
      Array(1.e-45, dtype=float32, weak_type=True)
      >>> lax.nextafter(0.0, 1.0) * 1  # but are flushed to zero
      Array(0., dtype=float32, weak_type=True)

    For the smallest usable (i.e. normal) float, use ``tiny`` of ``jnp.finfo``.
  """
  x1, x2 = core.auto_insert_reshard(x1, x2)
  return nextafter_p.bind(x1, x2)


def nextafter(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Return element-wise next floating point value after ``x`` towards ``y``.

  JAX implementation of :obj:`numpy.nextafter`.

  Args:
    x: scalar or array. Specifies the value after which the next number is found.
    y: scalar or array. Specifies the direction towards which the next number is
      found. ``x`` and ``y`` should either have same shape or be broadcast
      compatible.

  Returns:
    An array containing the next representable number of ``x`` in the direction
    of ``y``.

  Examples:
    >>> jnp.nextafter(2, 1)  # doctest: +SKIP
    Array(1.9999999, dtype=float32, weak_type=True)
    >>> x = jnp.array([3, -2, 1])
    >>> y = jnp.array([2, -1, 2])
    >>> jnp.nextafter(x, y)  # doctest: +SKIP
    Array([ 2.9999998, -1.9999999,  1.0000001], dtype=float32)
  """
  return lax.nextafter(*promote_args_inexact("nextafter", x, y))

