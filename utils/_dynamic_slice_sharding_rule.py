
def _dynamic_slice_sharding_rule(operand, *starts_and_dyn_sizes, slice_sizes):
  out_shape = _dynamic_slice_shape_rule(
      operand, *starts_and_dyn_sizes, slice_sizes=slice_sizes)
  return _get_sharding_for_varying_out_shape(out_shape, operand, 'dynamic_slice')

