
def reduce_prod(operand: ArrayLike, axes: Sequence[int]) -> Array:
  """Compute the product of elements over one or more array axes.

  Args:
    operand: array over which to sum. Must have numerical dtype.
    axes: sequence of zero or more unique integers specifying the axes over
      which to sum. Each entry must satisfy ``0 <= axis < operand.ndim``.

  Returns:
    An array of the same dtype as ``operand``, with shape corresponding
    to the dimensions of ``operand.shape`` with ``axes`` removed.

  Notes:
    Unlike :func:`jax.numpy.prod`, :func:`jax.lax.reduce_prod` does not upcast
    narrow-width types for accumulation, so products of 8-bit or 16-bit types
    may be subject to rounding errors.

  See also:
    - :func:`jax.numpy.prod`: more flexible NumPy-style product API, built
      around :func:`jax.lax.reduce_prod`.
    - Other low-level :mod:`jax.lax` reduction operators:
      :func:`jax.lax.reduce_sum`, :func:`jax.lax.reduce_max`, :func:`jax.lax.reduce_min`,
      :func:`jax.lax.reduce_and`, :func:`jax.lax.reduce_or`, :func:`jax.lax.reduce_xor`.
  """
  return reduce_prod_p.bind(operand, axes=tuple(axes))

