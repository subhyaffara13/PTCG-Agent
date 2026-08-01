
def _array_ir_types(aval: core.ShapedArray) -> ir.Type:
  aval = core.physical_aval(aval)
  if not core.is_constant_shape(aval.shape):
    return _dynamic_array_ir_types(aval)
  return ir.RankedTensorType.get(aval.shape, dtype_to_ir_type(aval.dtype))

