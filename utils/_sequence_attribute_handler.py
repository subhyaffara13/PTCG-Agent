
def _sequence_attribute_handler(val: Sequence[Any]) -> ir.Attribute:
  return ir.ArrayAttr.get([ir_attribute(v) for v in val])

