
def _splat(x: ir.Value, shape: Sequence[int]) -> ir.Value:
  if isinstance(x.type, ir.RankedTensorType):
    raise TypeError("cannot splat a tensor")
  if not shape:
    return x
  return tt_dialect.splat(ir.RankedTensorType.get(shape, x.type), x)

