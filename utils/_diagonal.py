
def _diagonal(self: Array, offset: int = 0, axis1: int = 0, axis2: int = 1) -> Array:
  """Return the specified diagonal from the array.

  Refer to :func:`jax.numpy.diagonal` for the full documentation.
  """
  return lax_numpy.diagonal(self, offset=offset, axis1=axis1, axis2=axis2)

