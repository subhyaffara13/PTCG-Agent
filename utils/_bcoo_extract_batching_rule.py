
def _bcoo_extract_batching_rule(batched_args, batch_dims, *, assume_unique):
  indices, arr = batched_args
  assert any(b is not None for b in batch_dims)
  if batch_dims[0] is None:
    bdim = batch_dims[1]
    indices = lax.expand_dims(indices, (bdim,))
  elif batch_dims[1] is None:
    # TODO(jakevdp) can we handle this case without explicit broadcasting?
    bdim = batch_dims[0]
    result_shape = list(arr.shape)
    result_shape.insert(bdim, indices.shape[bdim])
    arr = lax.broadcast_in_dim(arr, result_shape, (bdim,))
  else:
    if batch_dims[0] != batch_dims[1]:
      raise NotImplementedError("bcoo_extract with unequal batch dimensions.")
    bdim = batch_dims[0]
  n_batch = indices.ndim - 2
  if bdim >= n_batch:
    raise ValueError(f"{batch_dims=} out of range for indices with {n_batch=}")
  return _bcoo_extract(indices, arr, assume_unique=assume_unique), bdim

