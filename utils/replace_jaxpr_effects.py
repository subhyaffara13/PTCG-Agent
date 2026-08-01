
def replace_jaxpr_effects(jaxpr: ClosedJaxpr, effects: Effects):
  return _replace_jaxpr_effects(jaxpr, frozenset(effects))

