
def _enum_attr(e):
  return ir.IntegerAttr.get(ir.IntegerType.get_unsigned(8), e.value)

