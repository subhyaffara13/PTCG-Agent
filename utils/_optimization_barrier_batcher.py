
def _optimization_barrier_batcher(batched_args, batch_dims, **params):
  return optimization_barrier_p.bind(*batched_args, **params), batch_dims

