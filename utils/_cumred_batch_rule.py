
def _cumred_batch_rule(prim, batched_args, batch_dims, *, axis: int,
                       reverse: bool):
  operand, = batched_args
  bdim, = batch_dims
  axis = axis if axis < bdim else axis + 1
  return prim.bind(operand, axis=axis, reverse=reverse), bdim

