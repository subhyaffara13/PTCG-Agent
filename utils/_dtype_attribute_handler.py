
def _dtype_attribute_handler(dtype: np.dtype | np.generic) -> ir.Attribute:
  return ir.TypeAttr.get(dtype_to_ir_type(dtype))

