
def _round(self: Array, decimals: int = 0, out: None = None) -> Array:
  """Round array elements to a given decimal.

  Refer to :func:`jax.numpy.round` for full documentation.
  """
  return lax_numpy.round(self, decimals=decimals, out=out)

