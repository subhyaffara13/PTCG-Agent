
def _batch_jaxpr_axes(closed_jaxpr: core.ClosedJaxpr,
                      axis_data: AxisData,
                      in_axes: Sequence[int], out_axes_dest: Sequence[int]):
  f = lu.wrap_init(core.jaxpr_as_fun(closed_jaxpr),
                   debug_info=closed_jaxpr.jaxpr.debug_info)
  f, out_axes = _batch_jaxpr_inner(f, axis_data)
  f, out_batched = _match_axes_jaxpr(f, axis_data, out_axes_dest, out_axes)
  f = _batch_jaxpr_outer(f, axis_data, in_axes)
  avals_in = [core.unmapped_aval(axis_data.size, b, aval,
                                 axis_data.explicit_mesh_axis)
              if b is not None
              else aval for aval, b in unsafe_zip(closed_jaxpr.in_avals, in_axes)]
  jaxpr_out, _, consts = pe.trace_to_jaxpr_dynamic(f, avals_in)
  return core.ClosedJaxpr(jaxpr_out, consts), out_batched()

