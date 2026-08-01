
def _bcoo_todense_batching_rule(batched_args, batch_dims, *, spinfo):
  data, indices, spinfo = _bcoo_batch_dims_to_front(batched_args, batch_dims, spinfo)
  return _bcoo_todense(data, indices, spinfo=spinfo), 0

