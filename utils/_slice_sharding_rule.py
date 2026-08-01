
def _slice_sharding_rule(operand, *, start_indices, limit_indices, strides):
  # TODO(yashkatariya): Once JAX supports uneven sharding at the top level,
  # change this logic to `return operand.sharding` directly.
  out_shape = _slice_shape_rule(operand, start_indices=start_indices,
                                limit_indices=limit_indices, strides=strides)
  return _get_sharding_for_varying_out_shape(out_shape, operand, 'slicing')

