
def _prune_closed_jaxpr_outputs(
    jaxpr: ClosedJaxpr, used_outputs: tuple[bool, ...]
) -> ClosedJaxpr:
  return ClosedJaxpr(_prune_jaxpr_outputs(jaxpr.jaxpr, used_outputs),
                     jaxpr.consts)

