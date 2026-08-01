
def _bcast_to(a: ir.Value, shape: Sequence[int]) -> ir.Value:
  if not isinstance(a.type, ir.RankedTensorType):
    if not shape:
      return a
    return tt_dialect.splat(ir.RankedTensorType.get(shape, a.type), a)
  else:
    a_type = ir.RankedTensorType(a.type)
    if a_type.shape == [*shape]:
      return a
    for _ in range(a_type.rank, len(shape)):
      a = _expand_dims(a, 0)
    if a_type.rank != len(shape) or not all(
        a_type.shape[i] in (dim, 1) for i, dim in enumerate(shape)
    ):
      raise ValueError(f"Cannot broadcast from {a_type.shape} to {[*shape]}")
    return tt_dialect.broadcast(
        ir.RankedTensorType.get(shape, a_type.element_type, a_type.encoding), a
    )

