
def _squeeze_batch_rule(batched_args, batch_dims, *, dimensions):
  operand, = batched_args
  bdim, = batch_dims
  operand = batching.moveaxis(operand, bdim, 0)
  dimensions = tuple(np.add(1, dimensions))

  result_shape = _compute_squeeze_shape(operand.shape, dimensions)
  bdim_out = canonicalize_axis(0, len(result_shape))
  return squeeze(operand, dimensions=dimensions), bdim_out

