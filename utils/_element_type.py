
def _element_type(t: ir.Type) -> ir.Type:
  if isinstance(t, ir.RankedTensorType):
    return ir.RankedTensorType(t).element_type
  else:
    return t

