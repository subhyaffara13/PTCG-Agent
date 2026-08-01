
def _bcsr_batch_dims_to_front(batched_args, batch_dims, spinfo, batch_size=None):
  data, indices, indptr = batched_args
  data_bdim, indices_bdim, indptr_bdim = batch_dims
  n_batch = indices.ndim - 1 + int(indices_bdim is None)
  if not all(b is None or 0 <= b < n_batch for b in batch_dims):
    raise NotImplementedError("batch_dims must be None or satisfy 0 < dim < n_batch. "
                              f"Got {batch_dims=} for {n_batch=}.")
  batched_data, batched_indices, batched_indptr = (
      lax.expand_dims(arg, [0]) if bdim is None else jnp.moveaxis(arg, bdim, 0)
      for arg, bdim in [(data, data_bdim), (indices, indices_bdim), (indptr, indptr_bdim)])
  if batch_size is None:
    batch_size = max(arg.shape[dim] for arg, dim in zip(batched_args, batch_dims) if dim is not None)
  batched_spinfo = SparseInfo((batch_size, *spinfo.shape),
                              indices_sorted=spinfo.indices_sorted,
                              unique_indices=spinfo.unique_indices)
  return batched_data, batched_indices, batched_indptr, batched_spinfo

