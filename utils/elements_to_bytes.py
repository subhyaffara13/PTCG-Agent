
def elements_to_bytes(offset: ir.Value, element_bitwidth: int) -> ir.Value:
  """Convert an element-based linear offset to a byte-based offset."""
  index_ty = offset.type

  if element_bitwidth > 8:
    return arith.muli(offset, c(element_bitwidth // 8, index_ty))
  elif element_bitwidth < 8:
    return arith.divsi(offset, c(8 // element_bitwidth, index_ty))
  else:
    return offset

