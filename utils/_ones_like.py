
def _ones_like(x: ir.Value) -> ir.Value:
  return _full(x.type, 1)

