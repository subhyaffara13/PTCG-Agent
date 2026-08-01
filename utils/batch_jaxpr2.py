
def batch_jaxpr2(
    closed_jaxpr: core.ClosedJaxpr,
    axis_data,
    in_axes: tuple[int | NotMapped, ...],
  ) -> tuple[core.ClosedJaxpr, tuple[int | NotMapped, ...]]:
  return _batch_jaxpr2(closed_jaxpr, axis_data, tuple(in_axes))

