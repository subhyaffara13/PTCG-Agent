
def _validate_bcsr_indices(indices: jax.Array, indptr: jax.Array,
                           shape: Sequence[int]) -> BCSRProperties:
  assert jnp.issubdtype(indices.dtype, jnp.integer)
  assert jnp.issubdtype(indptr.dtype, jnp.integer)
  shape = tuple(shape)

  nse = indices.shape[-1]
  n_batch = indices.ndim - 1
  n_dense = len(shape) - n_batch - 2
  assert n_dense >= 0

  if not _compatible(indices.shape[:n_batch], shape[:n_batch]):
    raise ValueError(f"indices batch dimensions not compatible for {indices.shape=}, {shape=}")
  if not _compatible(indptr.shape[:n_batch], shape[:n_batch]):
    raise ValueError(f"indptr batch dimensions not compatible for {indptr.shape=}, {shape=}")
  if indptr.shape[n_batch:] != (shape[n_batch] + 1,):
    raise ValueError("indptr shape must match the matrix shape plus 1.")

  return BCSRProperties(n_batch=n_batch, n_dense=n_dense, nse=nse)

