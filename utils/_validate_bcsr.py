
def _validate_bcsr(data: jax.Array, indices: jax.Array,
                   indptr: jax.Array, shape: Sequence[int]) -> BCSRProperties:
  props = _validate_bcsr_indices(indices, indptr, shape)
  shape = tuple(shape)
  n_batch, n_dense, nse = props.n_batch, props.n_dense, props.nse
  n_sparse = len(shape) - n_batch - n_dense
  if n_sparse != 2:
    raise ValueError("BCSR array must have 2 sparse dimensions; "
                     f"{n_sparse} is given.")
  if not _compatible(data.shape[:n_batch], shape[:n_batch]):
    raise ValueError(f"data batch dimensions not compatible for {data.shape=}, {shape=}")
  if data.shape[-(n_dense + 1):] != (nse,) + shape[n_batch + 2:]:
    raise ValueError(f"Invalid {data.shape=} for {nse=}, {n_batch=}, {n_dense=}")
  return props

