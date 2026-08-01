
def _ir_cast(
    src: ir.Value,
    dst_type: ir.Type,
    *,
    signed: bool,
    dst_signed: bool = False,
    compute_capability: int | None = None,
) -> ir.Value:
  if isinstance(src.type, ir.RankedTensorType) and not isinstance(
      dst_type, ir.RankedTensorType
  ):
    src_type = ir.RankedTensorType(src.type)
    dst_type = ir.RankedTensorType.get(
        src_type.shape,
        dst_type,
        src_type.encoding,
    )
  if src.type == dst_type:
    return src

  src_element_type = _element_type(src.type)
  dst_element_type = _element_type(dst_type)

  for dtype, dtype_name, is_supported in _UNSUPPORTED_CAST_DTYPES:
    if isinstance(src_element_type, dtype):
      if not is_supported(compute_capability):
        raise NotImplementedError(f"cannot cast from `{dtype_name}`")
    if isinstance(dst_element_type, dtype):
      if not is_supported(compute_capability):
        raise NotImplementedError(f"cannot cast to `{dtype_name}`")

  if isinstance(src_element_type, (ir.F16Type, ir.BF16Type)) and not isinstance(
      dst_element_type, ir.F32Type
  ):
    return _ir_cast(
        _ir_cast(src, ir.F32Type.get(), signed=False),
        dst_type, signed=False, dst_signed=dst_signed
    )

  if isinstance(src_element_type, ir.FloatType) and isinstance(
      dst_element_type, ir.FloatType
  ):
    return _float_float_cast(src, dst_type)

  if isinstance(src_element_type, ir.IntegerType) and isinstance(
      dst_element_type, ir.IntegerType
  ):
    return _int_int_cast(src, dst_type, signed=signed)

  if isinstance(src_element_type, ir.FloatType) and isinstance(
      dst_element_type, ir.IntegerType
  ):
    return _float_int_cast(src, dst_type, signed=dst_signed)
  if isinstance(src_element_type, ir.IntegerType) and isinstance(
      dst_element_type, ir.FloatType
  ):
    return _int_float_cast(src, dst_type, signed=signed)

  if _is_triton_pointer_type(src_element_type) and isinstance(
      dst_element_type, ir.IntegerType
  ):
    if dst_element_type.width == 64:
      return tt_dialect.ptr_to_int(dst_type, src)
    elif dst_element_type.width == 1:
      x = _ir_cast(src, ir.IntegerType.get_signless(64), signed=signed)
      zero = _zeros_like(x)
      return _ir_cast(_not_equal(x, zero, signed=signed), dst_type, signed=signed)
  if isinstance(src_element_type, ir.IntegerType) and _is_triton_pointer_type(
      dst_element_type
  ):
    return tt_dialect.int_to_ptr(dst_type, src)
  if _is_triton_pointer_type(src_element_type) and _is_triton_pointer_type(
      dst_element_type
  ):
    return tt_dialect.bitcast(dst_type, src)

  raise NotImplementedError(f"cannot cast {src} to {dst_type}")

