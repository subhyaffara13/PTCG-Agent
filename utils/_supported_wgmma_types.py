
def _supported_wgmma_types(dtype, abtype) -> bool:
  input_types_are = lambda ty: isinstance(abtype, ty)
  f16_acc_types = (ir.F16Type, ir.Float8E5M2Type, ir.Float8E4M3FNType)
  if isinstance(dtype, ir.F32Type):
    return any(input_types_are(ty) for ty in (ir.FloatTF32Type, ir.BF16Type, *f16_acc_types))
  elif isinstance(dtype, ir.F16Type):
    return any(input_types_are(ty) for ty in f16_acc_types)
  elif (
      isinstance(dtype, ir.IntegerType)
      and dtype.width == 32
      and dtype.is_signless
  ):
    return input_types_are(ir.IntegerType)
  else:
    return False

