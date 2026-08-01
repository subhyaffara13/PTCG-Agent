
def _convert_element_type_batching_rule(
    axis_data, batched_args, batch_dims, *, new_dtype, weak_type, sharding):
  operand, = batched_args
  operand_bdim, = batch_dims
  if operand_bdim is not None:
    if sharding is not None:
      sharding = batching.get_sharding_for_vmap(axis_data, sharding, operand_bdim)
    new_params = dict(new_dtype=new_dtype, weak_type=weak_type, sharding=sharding)
    return convert_element_type_p.bind(operand, **new_params), operand_bdim
  else:
    out = convert_element_type_p.bind(operand, new_dtype=new_dtype,
                                      weak_type=weak_type, sharding=sharding)
    return out, None

