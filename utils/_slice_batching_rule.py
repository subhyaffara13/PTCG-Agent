
def _slice_batching_rule(batched_args, batch_dims, *, start_indices,
                         limit_indices, strides):
  operand, = batched_args
  bdim, = batch_dims

  new_start_indices = list(start_indices)
  new_start_indices.insert(bdim, 0)

  new_limit_indices = list(limit_indices)
  new_limit_indices.insert(bdim, operand.shape[bdim])

  if strides is None:
    new_strides = None
  else:
    new_strides = list(strides)
    new_strides.insert(bdim, 1)

  out = slice(operand, new_start_indices, new_limit_indices, new_strides)
  return out, bdim

