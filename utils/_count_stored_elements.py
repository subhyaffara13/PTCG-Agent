
def _count_stored_elements(mat: Array, n_batch: int = 0, n_dense: int = 0) -> Array:
  """Return the number of stored elements (nse) of the given dense matrix."""
  return _count_stored_elements_per_batch(mat, n_batch, n_dense).max(initial=0)

