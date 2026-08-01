
def _floordiv(x: ir.Value, y: ir.Value, *, signed: bool) -> ir.Value:
  assert x.type == y.type, (str(x.type), str(y.type))
  x_element_type = _element_type(x.type)
  if isinstance(x_element_type, (ir.F32Type, ir.F64Type)):
    return arith_dialect.divf(x, y)
  if not isinstance(x_element_type, ir.IntegerType):
    raise NotImplementedError(f"unsupported types: {x.type} and {y.type}")
  if signed:
    return arith_dialect.divsi(x, y)
  else:
    return arith_dialect.divui(x, y)

