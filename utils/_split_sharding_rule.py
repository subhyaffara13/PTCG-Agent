
def _split_sharding_rule(operand, *, sizes, axis):
  # TODO(yashkatariya): Once JAX supports uneven sharding at the top level,
  # change this logic to `return operand.sharding` directly.
  out_shapes = _split_shape_rule(operand, sizes=sizes, axis=axis)
  return [slicing._get_sharding_for_varying_out_shape(out_sh, operand, 'split')
          for out_sh in out_shapes]

