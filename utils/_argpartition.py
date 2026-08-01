
def _argpartition(self: Array, kth: int, axis: int = -1) -> Array:
  """Return the indices that partially sort the array.

  Refer to :func:`jax.numpy.argpartition` for the full documentation.
  """
  return sorting.argpartition(self, kth=kth, axis=axis)

