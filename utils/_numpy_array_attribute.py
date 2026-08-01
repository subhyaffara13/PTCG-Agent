
def _numpy_array_attribute(x: np.ndarray | np.generic) -> ir.Attribute:
  element_type = dtype_to_ir_type(x.dtype)
  shape = x.shape
  x = np.ascontiguousarray(x)
  return ir.DenseElementsAttr.get(x, type=element_type, shape=shape)

