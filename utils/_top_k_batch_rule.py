
def _top_k_batch_rule(batched_args, batch_dims, *, k, axis):
  operand, = batched_args
  bdim, = batch_dims
  if bdim <= axis:
    axis += 1
  return top_k(operand, k=k, axis=axis), (bdim, bdim)

