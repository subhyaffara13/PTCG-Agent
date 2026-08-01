
def vectorized_batcher(prim, axis_data, batched_args, batch_dims, **params):
  assert not prim.multiple_results
  if all(d is None for d in batch_dims):
    return prim.bind(*batched_args, **params), None
  assert all(batch_dims[0] == bd for bd in batch_dims[1:]), batch_dims
  return prim.bind(*batched_args, **params), batch_dims[0]

