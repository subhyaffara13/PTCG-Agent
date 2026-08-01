
def _swapaxes(self: Array, axis1: int, axis2: int) -> Array:
  """Swap two axes of an array.

  Refer to :func:`jax.numpy.swapaxes` for full documentation.
  """
  return lax_numpy.swapaxes(self, axis1=axis1, axis2=axis2)

