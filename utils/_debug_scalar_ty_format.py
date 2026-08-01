
def _debug_scalar_ty_format(arg):
  if isinstance(arg.type, ir.IndexType):
    return "%llu", arg
  if isinstance(arg.type, ir.IntegerType):
    if ir.IntegerType(arg.type).width < 64:
      arg = arith.extui(ir.IntegerType.get_signless(64), arg)
    return "%llu", arg
  if isinstance(arg.type, ir.F32Type):
    return "%f", arg
  if isinstance(arg.type, ir.Float8E8M0FNUType):
    return "%u", arith.extui(
        ir.IntegerType.get_signless(32),
        arith.bitcast(ir.IntegerType.get_signless(8), arg),
    )
  if isinstance(arg.type, ir.BF16Type) or isinstance(arg.type, ir.F16Type):
    arg = arith.extf(ir.F32Type.get(), arg)
    return "%f", arg
  raise NotImplementedError(f"Can't print the type {arg.type}")

