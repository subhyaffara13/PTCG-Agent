
def prune_closed_jaxpr_outputs(
    jaxpr: ClosedJaxpr, used_outputs: Sequence[bool]
) -> ClosedJaxpr:
  return _prune_closed_jaxpr_outputs(jaxpr, tuple(used_outputs))

