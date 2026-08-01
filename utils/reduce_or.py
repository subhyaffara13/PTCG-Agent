
def reduce_or(operand: ArrayLike, axes: Sequence[int]) -> Array:
  """Compute the bitwise OR of elements over one or more array axes.

  Args:
    operand: array over which to compute the reduction. Must have boolean
      or integer dtype.
    axes: sequence of zero or more unique integers specifying the axes over
      which to reduce. Each entry must satisfy ``0 <= axis < operand.ndim``.

  Returns:
    An array of the same dtype as ``operand``, with shape corresponding
    to the dimensions of ``operand.shape`` with ``axes`` removed.

  See also:
    - :func:`jax.numpy.bitwise_or.reduce`: more flexible NumPy-style logical
      reduction API, built around :func:`jax.lax.reduce_or`.
    - Other low-level :mod:`jax.lax` reduction operators:
      :func:`jax.lax.reduce_sum`, :func:`jax.lax.reduce_prod`, :func:`jax.lax.reduce_max`,
      :func:`jax.lax.reduce_min`, :func:`jax.lax.reduce_and`, :func:`jax.lax.reduce_xor`.
  """
  return reduce_or_p.bind(operand, axes=tuple(axes))

