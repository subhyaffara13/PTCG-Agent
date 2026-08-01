
def _dynamic_array_ir_types(aval: core.ShapedArray) -> ir.Type:
  dyn_size = ir.ShapedType.get_dynamic_size()
  shape = [d if type(d) is int else dyn_size for d in aval.shape]
  return ir.RankedTensorType.get(shape, dtype_to_ir_type(aval.dtype))

