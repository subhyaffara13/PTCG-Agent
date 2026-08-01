
def _conjugate(self: Array) -> Array:
  """Return the complex conjugate of the array.

  Refer to :func:`jax.numpy.conjugate` for the full documentation.
  """
  return ufuncs.conjugate(self)

