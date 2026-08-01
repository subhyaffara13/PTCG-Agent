
def eqn_effects(jaxpr, invars) -> Effects:
  return resolve_input_effects(positional_effects(jaxpr), invars)

