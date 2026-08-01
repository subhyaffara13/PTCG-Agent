
def get_join_type(old_type: ir.RankedTensorType):
  shape = old_type.shape
  shape.append(2)
  return ir.RankedTensorType.get(shape, old_type.element_type, old_type.encoding)

