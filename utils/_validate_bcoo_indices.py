
def _validate_bcoo_indices(indices: Buffer, shape: Sequence[int]) -> BCOOProperties:
  assert jnp.issubdtype(indices.dtype, jnp.integer)
  shape = tuple(shape)
  nse, n_sparse = indices.shape[-2:]
  n_batch = len(indices.shape) - 2
  n_dense = len(shape) - n_batch - n_sparse
  assert n_dense >= 0
  if any(s1 not in (1, s2) for s1, s2 in safe_zip(indices.shape[:n_batch], shape[:n_batch])):
    raise ValueError(f"indices batch dimensions not compatible for {indices.shape=}, {shape=}")
  if indices.shape[n_batch:] != (nse, n_sparse):
    raise ValueError(f"Invalid ={indices.shape=} for {nse=}, {n_batch=}, {n_dense=}")
  return BCOOProperties(n_batch=n_batch, n_sparse=n_sparse, n_dense=n_dense, nse=nse)

