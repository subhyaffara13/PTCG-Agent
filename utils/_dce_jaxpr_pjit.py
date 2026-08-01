
def _dce_jaxpr_pjit(
    jaxpr: core.ClosedJaxpr, used_outputs: tuple[bool, ...]
) -> tuple[core.ClosedJaxpr, list[bool]]:
  new_jaxpr, used_inputs = pe.dce_jaxpr(jaxpr.jaxpr, used_outputs)
  return core.ClosedJaxpr(new_jaxpr, jaxpr.consts), used_inputs

