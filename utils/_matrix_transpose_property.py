
def _matrix_transpose_property(self: Array):
  """Compute the (batched) matrix transpose.

  Refer to :func:`jax.numpy.matrix_transpose` for details.
  """
  return lax_numpy.matrix_transpose(self)

