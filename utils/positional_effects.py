
def positional_effects(jaxpr) -> Effects:
  if isinstance(jaxpr, ClosedJaxpr):
    jaxpr = jaxpr.jaxpr
  if not any(isinstance(e, effects.JaxprInputEffect) for e in jaxpr.effects):
    return jaxpr.effects
  idx = {v: i for i, v in enumerate(jaxpr.invars)}
  out_effs = set()
  for eff in jaxpr.effects:
    if isinstance(eff, effects.JaxprInputEffect):
      i = idx.get(eff.input)
      if i is None:
        continue
      eff = eff.replace(i)
    out_effs.add(eff)
  return out_effs

