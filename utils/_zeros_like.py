
def _zeros_like(x: ir.Value) -> ir.Value:
  return _full(x.type, 0)

