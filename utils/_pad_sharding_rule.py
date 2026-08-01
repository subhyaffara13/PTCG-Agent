
def _pad_sharding_rule(operand, padding_value, *, padding_config):
  # TODO(yashkatariya): Once JAX supports uneven sharding at the top level,
  # change this logic to `return operand.sharding` directly.
  out_shape = _pad_shape_rule(operand, padding_value,
                              padding_config=padding_config)
  return slicing._get_sharding_for_varying_out_shape(
      out_shape, operand, 'padding')

