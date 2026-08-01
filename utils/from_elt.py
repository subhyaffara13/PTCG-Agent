
def from_elt(trace: BatchTrace, axis_size: AxisSize, mesh_axis: MeshAxis,
             sum_match: bool, i: int, x: Elt, spec: MapSpec) -> tuple[Vmappable, MapSpec]:
  handler = from_elt_handlers.get(type(x))
  if handler:
    def _cont(axis_size, elt, axis):
      return from_elt(trace, axis_size, mesh_axis, sum_match, i, elt, axis)[0]
    return handler(_cont, axis_size, x, spec), spec
  val, bdim = trace.to_batch_info(x)
  bdim_inferred = bdim if spec is infer else spec
  try:
    return matchaxis(trace.axis_data, bdim, spec, val,
                     sum_match=sum_match), bdim_inferred
  except SpecMatchError:
    raise SpecMatchError(i, x.batch_dim, spec) from None

