
def _move_mutable_consts(
    closed_jaxpr: core.ClosedJaxpr,
) -> tuple[core.ClosedJaxpr, list[core.Ref]]:
  jaxpr = closed_jaxpr.jaxpr
  hoist = [isinstance(c, core.Ref) for c in closed_jaxpr.consts]
  consts, in_mut = partition_list(hoist, closed_jaxpr.consts)
  constvars, mutvars = partition_list(hoist, jaxpr.constvars)
  invars = (*jaxpr.invars, *mutvars)
  effects = pe.make_jaxpr_effects(constvars, invars, jaxpr.outvars, jaxpr.eqns)
  # TODO(mattjj): debug_info must be updated...
  jaxpr = closed_jaxpr.jaxpr.replace(
      constvars=constvars, invars=invars, effects=effects,
      debug_info=closed_jaxpr.debug_info.with_unknown_names())
  return core.ClosedJaxpr(jaxpr, consts), in_mut

