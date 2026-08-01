
def _count_stored_elements_per_batch(mat: Array, n_batch: int = 0, n_dense: int = 0) -> Array:
  """Return per-batch number of stored elements (nse) of a dense matrix."""
  mat = jnp.asarray(mat)
  mask = (mat != 0)
  if n_dense > 0:
    mask = mask.any(tuple(-(i + 1) for i in range(n_dense)))
  mask = mask.sum(tuple(range(n_batch, mask.ndim)))
  return mask

