
def _cached_closed_call_dce_instantiate(jaxpr_: core.ClosedJaxpr,
                                        used_outputs: tuple[bool, ...]
                                        ) -> tuple[core.ClosedJaxpr, list[bool]]:
  jaxpr, consts = jaxpr_.jaxpr, jaxpr_.consts
  new_jaxpr, used_inputs = pe.dce_jaxpr(
      jaxpr.replace(debug_info=jaxpr.debug_info.with_unknown_names()),
      used_outputs, True)
  return core.ClosedJaxpr(new_jaxpr, consts), used_inputs

