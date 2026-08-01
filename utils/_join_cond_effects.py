
def _join_cond_effects(branches: Sequence[core.ClosedJaxpr]) -> effects.Effects:
  joined_effects = set()
  for b in branches:
    for eff in core.positional_effects(b):
      if isinstance(eff, effects.JaxprInputEffect):
        # Offset index to handle predicate
        eff = eff.replace(eff.input + 1)
      joined_effects.add(eff)
  return joined_effects

