
def _stop_gradient_batch_rule(batched_args, batch_dims):
  x, = batched_args
  dim, = batch_dims
  return stop_gradient(x), dim

