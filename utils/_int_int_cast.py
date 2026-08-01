
def _int_int_cast(src: ir.Value, dst_type: ir.Type, signed: bool) -> ir.Value:
  src_element_type = ir.IntegerType(_element_type(src.type))
  dst_element_type = ir.IntegerType(_element_type(dst_type))
  assert src_element_type != dst_element_type
  if dst_element_type.width == 1:
    return _not_equal(src, _zeros_like(src), signed=signed)

  if src_element_type.width == dst_element_type.width:
    return arith_dialect.bitcast(dst_type, src)
  elif src_element_type.width > dst_element_type.width:
    return arith_dialect.trunci(dst_type, src)
  elif signed and src_element_type.width != 1:
    return arith_dialect.extsi(dst_type, src)
  else:
    return arith_dialect.extui(dst_type, src)

