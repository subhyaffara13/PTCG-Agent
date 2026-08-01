
def resolve_input_effects(effs, invars) -> Effects:
  if not any(isinstance(e, effects.JaxprInputEffect) and isinstance(e.input, int)
             for e in effs):
    return effs
  out_effs = set()
  for eff in effs:
    if isinstance(eff, effects.JaxprInputEffect) and isinstance(eff.input, int):
      invar = invars[eff.input]
      if isinstance(invar, Literal):
        continue
      eff = eff.replace(invar)
    out_effs.add(eff)
  return out_effs

