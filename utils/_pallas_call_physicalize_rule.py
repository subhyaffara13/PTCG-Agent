
def _pallas_call_physicalize_rule(
    ctx: Context, *args, jaxpr, grid_mapping: pallas_core.GridMapping, **kwargs
):
  _assert_no_fusion_types(ctx.avals_in)
  _assert_no_fusion_types(ctx.avals_out)
  with grid_mapping.trace_env():
    new_jaxpr = physicalize_closed_jaxpr(core.ClosedJaxpr(jaxpr, ()))
  if diff := len(new_jaxpr.jaxpr.invars) - len(jaxpr.invars):
    num_scratch_avals = len(grid_mapping.scratch_avals) + diff
    new_scratch_avals = tuple(v.aval for v in
                              new_jaxpr.jaxpr.invars[-num_scratch_avals:])
    grid_mapping = grid_mapping.replace(
        scratch_avals=new_scratch_avals
    )
  return pallas_call.pallas_call_p.bind(
      *args, jaxpr=new_jaxpr.jaxpr, grid_mapping=grid_mapping, **kwargs
  )

