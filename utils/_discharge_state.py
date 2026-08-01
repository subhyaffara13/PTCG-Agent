
def _discharge_state(
    closed_jaxpr: core.ClosedJaxpr,
    should_discharge: tuple[bool, ...],
    lower: bool,
 ) -> core.ClosedJaxpr:
  in_avals = [
      v.aval.inner_aval
      if isinstance(v.aval, AbstractRef) and d
      else v.aval for v, d in zip(closed_jaxpr.invars, should_discharge)]
  eval_jaxpr = lu.wrap_init(
      partial(_eval_jaxpr_discharge_state,
              closed_jaxpr.jaxpr, should_discharge, closed_jaxpr.consts),
      debug_info=closed_jaxpr.debug_info.with_unknown_names())
  new_jaxpr, _ , new_consts = pe.trace_to_jaxpr_dynamic(
      eval_jaxpr, in_avals, lower=lower)
  return core.ClosedJaxpr(new_jaxpr, new_consts)

