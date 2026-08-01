
def _is_ir_values(x: IrValues) -> bool:
  """Returns true if `x` is an ir.Value or tuple of ir.Values"""
  if isinstance(x, ir.Value):
    return True
  return (isinstance(x, tuple) and len(x) != 1
          and all(isinstance(v, ir.Value) for v in x))

