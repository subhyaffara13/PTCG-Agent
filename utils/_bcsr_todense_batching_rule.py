
def _bcsr_todense_batching_rule(batched_args, batch_dims, *, spinfo):
  data, indices, indptr, spinfo = _bcsr_batch_dims_to_front(batched_args, batch_dims, spinfo)
  return _bcsr_todense(data, indices, indptr, spinfo=spinfo), 0

