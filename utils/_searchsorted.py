
def _searchsorted(self: Array, v: ArrayLike, side: str = 'left',
                  sorter: ArrayLike | None = None, *, method: str = 'scan') -> Array:
  """Perform a binary search within a sorted array.

  Refer to :func:`jax.numpy.searchsorted` for full documentation."""
  return lax_numpy.searchsorted(self, v, side=side, sorter=sorter, method=method)

