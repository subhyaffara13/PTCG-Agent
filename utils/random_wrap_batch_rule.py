
def random_wrap_batch_rule(batched_args, batch_dims, *, impl):
  x, = batched_args
  d, = batch_dims
  x = batching.bdim_at_front(x, d, 1)
  return random_wrap(x, impl=impl), 0

