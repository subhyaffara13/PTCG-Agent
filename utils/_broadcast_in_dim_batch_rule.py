
def _broadcast_in_dim_batch_rule(axis_data, batched_args, batch_dims, shape,
                                 broadcast_dimensions, sharding):
  # `shape` is the target shape. broadcast_dimensions gives indices where
  # dimensions of the input have to go: dimension i of the input becomes
  # dimension broadcast_dimensions[i] of the output.
  operand, = batched_args
  operand_bdim, = batch_dims
  if operand_bdim is None:
    out = broadcast_in_dim_p.bind(
        operand, shape=shape, broadcast_dimensions=broadcast_dimensions,
        sharding=sharding)
    return out, None
  new_operand = batching.moveaxis(operand, operand_bdim, 0)
  new_broadcast_dimensions = (0,) + tuple(np.add(1, broadcast_dimensions))
  new_shape = (operand.shape[operand_bdim],) + shape

  if sharding is not None:
    sharding = batching.get_sharding_for_vmap(axis_data, sharding, 0)

  result = broadcast_in_dim(new_operand, new_shape, new_broadcast_dimensions,
                            out_sharding=sharding)
  return result, 0

