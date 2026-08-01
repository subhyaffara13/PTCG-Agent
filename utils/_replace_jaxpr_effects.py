
def _replace_jaxpr_effects(jaxpr: ClosedJaxpr, effects: frozenset[Effect]):
  return jaxpr.replace(jaxpr=jaxpr.jaxpr.replace(effects=set(effects)))

