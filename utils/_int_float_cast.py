
def _int_float_cast(
    src: ir.Value, dst_type: ir.Type, *, signed: bool
) -> ir.Value:
  src_element_type = ir.IntegerType(_element_type(src.type))
  dst_element_type = _element_type(dst_type)
  if not isinstance(
      dst_element_type, (ir.BF16Type, ir.F16Type, ir.F32Type, ir.F64Type)
  ):
    raise NotImplementedError(f"cannot cast {src} tp {dst_type}")
  if src_element_type.width == 1 or not signed:
    return arith_dialect.uitofp(dst_type, src)
  else:
    return arith_dialect.sitofp(dst_type, src)

