
def _ptx_dtype_str(dtype: ir.Type, *, is_signed: bool | None = None) -> str:
  if isinstance(dtype, ir.Float8E4M3FNType):
    return "e4m3"
  elif isinstance(dtype, ir.Float8E5M2Type):
    return "e5m2"
  elif isinstance(dtype, ir.IntegerType):
    if is_signed is None:
      raise ValueError("is_signed must be specified for integer types")
    prefix = "s" if is_signed else "u"
    return f"{prefix}{dtype.width}"
  return str(dtype)

