
def _join_while_effects(body_jaxpr, cond_jaxpr, body_nconsts, cond_nconsts
                       ) -> effects.Effects:
  joined_effects = set()
  for eff in core.positional_effects(cond_jaxpr):
    if isinstance(eff, effects.JaxprInputEffect):
      index = eff.input
      if index >= cond_nconsts:
        index += body_nconsts
      eff = eff.replace(index)
    joined_effects.add(eff)
  for eff in core.positional_effects(body_jaxpr):
    if isinstance(eff, effects.JaxprInputEffect):
      eff = eff.replace(eff.input + cond_nconsts)
    joined_effects.add(eff)
  return joined_effects

