
def _reshape_batch_rule(axis_data, batched_args, batch_dims, *, new_sizes,
                        dimensions, sharding):
  operand, = batched_args
  bdim, = batch_dims
  if bdim is None:
    out = reshape_p.bind(operand, new_sizes=new_sizes, dimensions=dimensions,
                         sharding=sharding)
    return out, None
  operand = batching.moveaxis(operand, bdim, 0)
  if dimensions is not None:
    dimensions = (0,) + tuple(np.add(1, dimensions))

  if sharding is not None:
    sharding = batching.get_sharding_for_vmap(axis_data, sharding, 0)

  out = reshape(operand, operand.shape[:1] + new_sizes, dimensions,
                out_sharding=sharding)
  return out, 0

