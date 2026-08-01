
def prune_jaxpr_outputs(jaxpr: Jaxpr, used_outputs: Sequence[bool]) -> Jaxpr:
  return _prune_jaxpr_outputs_cached(jaxpr, tuple(used_outputs))

