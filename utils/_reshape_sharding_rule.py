
def _reshape_sharding_rule(operand, *, new_sizes, dimensions, sharding):
  if sharding is not None:
    return sharding
  if all(s is None for s in operand.sharding.spec.partitions):
    return operand.sharding
  non_1s_op_shape = [s for s in operand.shape if s != 1]
  non_1s_new_shape = [s for s in new_sizes if s != 1]
  if non_1s_op_shape == non_1s_new_shape:
    return _split_merge_singleton_dim_sharding_rule(operand, new_sizes)

  try:
    is_split, out_split = _split_on_one_axis(operand.shape, new_sizes)
  except ReshapeExplicitError:
    raise_reshape_error(operand, new_sizes)
  if is_split:
    return _split_an_axis_sharding_rule(operand, out_split, new_sizes,
                                        dimensions)

  try:
    is_merge, operand_merge = _merge_on_one_axis(operand, new_sizes)
  except ReshapeExplicitError:
    raise_reshape_error(operand, new_sizes)
  if is_merge:
    return _merge_an_axis_sharding_rule(operand, operand_merge, new_sizes,
                                        dimensions)
  raise_reshape_error(operand, new_sizes)

