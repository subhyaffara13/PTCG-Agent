
def _split_batch_rule(batched_args, batch_dims, *, sizes, axis):
  operand, = batched_args
  bdim, = batch_dims
  new_bdims = (bdim,) * len(sizes)
  out = split(operand, sizes=sizes, axis=axis + 1 if axis >= bdim else axis)
  return out, new_bdims

