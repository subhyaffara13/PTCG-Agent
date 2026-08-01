
def _expand_dims(x: ir.Value, axis: int) -> ir.Value:
  if not isinstance(x.type, ir.RankedTensorType):
    shape = list(ir.RankedTensorType(x.type).shape)
    shape.insert(axis, 1)
    return _splat(x, shape)
  return tt_dialect.expand_dims(x, axis)

