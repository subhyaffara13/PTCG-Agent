
def _truediv(x: ir.Value, y: ir.Value, *, signed: bool) -> ir.Value:
  assert x.type == y.type, (str(x.type), str(y.type))
  x_element_type = _element_type(x.type)
  if isinstance(x_element_type, ir.IntegerType):
    x_element_type = ir.F32Type.get()
    x = _int_float_cast(x, x_element_type, signed=signed)
    y = _int_float_cast(y, x_element_type, signed=signed)
  if isinstance(x_element_type, (ir.F32Type, ir.F64Type)):
    return arith_dialect.divf(x, y)
  raise NotImplementedError(f"unsupported types: {x.type} and {y.type}")

