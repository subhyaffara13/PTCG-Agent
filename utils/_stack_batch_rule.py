
def _stack_batch_rule(batched_args, batch_dims, *, axis):
  bdim = batch_dims[0]
  if all(b == bdim for b in batch_dims) and bdim is not None:
    if axis <= bdim:
      out_axis = axis
      out_bdim = bdim + 1
    else:
      out_axis = axis + 1
      out_bdim = bdim
    return stack_p.bind(*batched_args, axis=out_axis), out_bdim
  else:
    size = next(op.shape[bdim] for op, bdim in zip(batched_args, batch_dims)
                if bdim is not None)
    operands = [batching.moveaxis(op, bdim, 0) if bdim is not None
                else broadcast(op, (size,))
                for op, bdim in zip(batched_args, batch_dims)]
    return stack_p.bind(*operands, axis=axis + 1), 0

