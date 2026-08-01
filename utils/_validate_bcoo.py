
def _validate_bcoo(data: Buffer, indices: Buffer, shape: Sequence[int]) -> BCOOProperties:
  props = _validate_bcoo_indices(indices, shape)
  n_batch, n_sparse, n_dense, nse = props
  shape = tuple(shape)
  if any(s1 not in (1, s2) for s1, s2 in safe_zip(data.shape[:n_batch], shape[:n_batch])):
    raise ValueError(f"data batch dimensions not compatible for {data.shape=}, {shape=}")
  if data.shape[n_batch:] != (nse,) + shape[n_batch + n_sparse:]:
    raise ValueError(f"Invalid {data.shape=} for {nse=}, {n_batch=}, {n_dense=}")
  return props

