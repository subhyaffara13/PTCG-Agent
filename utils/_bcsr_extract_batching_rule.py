
def _bcsr_extract_batching_rule(batched_args, batch_dims):
  indices, indptr, arr = batched_args
  bdim_set = {b for b in batch_dims if b is not None}
  if len(bdim_set) != 1:
    # TODO(jakevdp): handle this by moving bdim to front?
    raise NotImplementedError("bcoo_extract with unequal batch dimensions.")
  bdim = next(iter(bdim_set))
  if batch_dims[0] is None:
    indices = lax.expand_dims(indices, (bdim,))
  if batch_dims[1] is None:
    indptr = lax.expand_dims(indptr, (bdim,))
  if batch_dims[2] is None:
    # TODO(jakevdp) can we handle this case without explicit broadcasting?
    result_shape = list(arr.shape)
    result_shape.insert(bdim, indices.shape[bdim])
    arr = lax.broadcast_in_dim(arr, result_shape, (bdim,))
  n_batch = indices.ndim - 1
  if bdim >= n_batch:
    raise ValueError(f"{batch_dims=} out of range for indices with {n_batch=}")
  return bcsr_extract(indices, indptr, arr), bdim

