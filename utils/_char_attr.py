
def _char_attr(c):
  return ir.IntegerAttr.get(ir.IntegerType.get_unsigned(8), ord(c))

