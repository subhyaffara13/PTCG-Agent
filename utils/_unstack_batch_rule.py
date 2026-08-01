
def _unstack_batch_rule(batched_args, batch_dims, *, axis):
  operand, = batched_args
  bdim, = batch_dims

  if bdim is None:
    return unstack(operand, axis=axis), (None,) * operand.shape[axis]

  if axis < bdim:
    out_axis = axis
    out_bdim = bdim - 1
  else:
    out_axis = axis + 1
    out_bdim = bdim

  results = unstack_p.bind(operand, axis=out_axis)
  return results, (out_bdim,) * len(results)

