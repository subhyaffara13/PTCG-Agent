
def _float_int_cast(
    src: ir.Value, dst_type: ir.Type, *, signed: bool
) -> ir.Value:
  src_element_type = _element_type(src.type)
  if not isinstance(src_element_type, (ir.BF16Type, ir.F16Type, ir.F32Type, ir.F64Type)):
    raise NotImplementedError(f"cannot cast {src} tp {dst_type}")
  dst_element_type = ir.IntegerType(_element_type(dst_type))
  if dst_element_type.width == 1:
    return _not_equal(src, _zeros_like(src), signed=signed)
  else:
    # We clamp the float value to the min/max integer destination value
    # in order to match JAX/XLA casting behavior. Note that this differs
    # from numpy casting behavior.
    if signed:
      maxint = 2**(dst_element_type.width-1) - 1
      minint = -2**(dst_element_type.width-1)
    else:
      maxint = 2**dst_element_type.width - 1
      minint = 0
    src = arith_dialect.minimumf(src, _full(src.type, maxint))
    src = arith_dialect.maximumf(src, _full(src.type, minint))
    if signed:
      return arith_dialect.fptosi(dst_type, src)
    else:
      return arith_dialect.fptoui(dst_type, src)

