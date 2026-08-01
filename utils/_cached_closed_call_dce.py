
def _cached_closed_call_dce(jaxpr_, used_outputs: tuple[bool, ...]
                            ) -> tuple[ClosedJaxpr, list[bool]]:
  jaxpr, consts = jaxpr_.jaxpr, jaxpr_.consts
  new_jaxpr, used_inputs = dce_jaxpr(jaxpr, used_outputs)
  return ClosedJaxpr(new_jaxpr, consts), used_inputs

