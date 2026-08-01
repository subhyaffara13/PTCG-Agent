
def _bcsr_fromdense_batching_rule(batched_args, batch_dims, *, nse, n_batch,
                                  n_dense, index_dtype):
  M, = batched_args
  bdim, = batch_dims
  if not (0 <= bdim <= n_batch):
    raise ValueError(f"Expected 0 < bdim <= n_batch; got {bdim=}, {n_batch=}")
  return _bcsr_fromdense(M, nse=nse, n_batch=n_batch + 1, n_dense=n_dense, index_dtype=index_dtype), (bdim, bdim, bdim)

