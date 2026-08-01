
def _float_float_cast(src: ir.Value, dst_type: ir.Type) -> ir.Value:
  src_element_type = ir.FloatType(_element_type(src.type))
  dst_element_type = ir.FloatType(_element_type(dst_type))
  if src_element_type.width == 8 or dst_element_type.width == 8:
    rounding = (
        tt_dialect.RoundingMode.RTNE if src_element_type.width > 8 else None
    )
    return tt_dialect.fp_to_fp(dst_type, src, rounding=rounding)
  if src_element_type.width > dst_element_type.width:
    return arith_dialect.truncf(dst_type, src)
  elif src_element_type.width < dst_element_type.width:
    return arith_dialect.extf(dst_type, src)
  else:
    raise NotImplementedError

