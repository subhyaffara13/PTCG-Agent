
def _rev_batch_rule(batched_args, batch_dims, *, dimensions):
  operand, = batched_args
  bdim, = batch_dims
  new_dimensions = [i + 1 if i >= bdim else i for i in dimensions]
  return rev(operand, new_dimensions), bdim

