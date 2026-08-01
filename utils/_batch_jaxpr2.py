
def _batch_jaxpr2(
    closed_jaxpr: core.ClosedJaxpr,
    axis_data,
    in_axes: tuple[int | NotMapped, ...],
  ) -> tuple[core.ClosedJaxpr, tuple[int | NotMapped, ...]]:
  f = lu.wrap_init(core.jaxpr_as_fun(closed_jaxpr),
                   debug_info=closed_jaxpr.jaxpr.debug_info)
  f, out_axes = _batch_jaxpr_inner(f, axis_data)
  f = _batch_jaxpr_outer(f, axis_data, in_axes)
  avals_in2 = []
  for aval, b in unsafe_zip(closed_jaxpr.in_avals, in_axes):
    if b is None:
      avals_in2.append(aval)
    else:
      aval = core.unmapped_aval(
          axis_data.size, b, aval, axis_data.explicit_mesh_axis)
      if axis_data.spmd_name is not None:
        if config._check_vma.value:
          mat = aval.mat.update(  # pyrefly: ignore[missing-attribute]
              varying=aval.mat.varying  | frozenset(axis_data.spmd_name))  # pyrefly: ignore[missing-attribute]
          aval = aval.update(manual_axis_type=mat)
      avals_in2.append(aval)
  jaxpr_out, _, consts = pe.trace_to_jaxpr_dynamic(f, avals_in2)
  return core.ClosedJaxpr(jaxpr_out, consts), out_axes()

