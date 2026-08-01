
def _gamma_batching_rule(batched_args, batch_dims, *, log_space):
  k, a = batched_args
  bk, ba = batch_dims
  size = next(
      t.shape[i] for t, i in zip(batched_args, batch_dims) if i is not None)
  k = batching.bdim_at_front(k, bk, size)
  a = batching.bdim_at_front(a, ba, size)
  return random_gamma_p.bind(k, a, log_space=log_space), 0

