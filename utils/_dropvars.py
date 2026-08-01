
def _dropvars(jaxpr: Jaxpr) -> dict[Var, Literal_['_']]:
  varnames: dict[Var, Literal_['_']] = {}
  used: set[Var] = {atom for atom in jaxpr.outvars if isinstance(atom, Var)}
  for eqn in jaxpr.eqns[::-1]:
    for v in eqn.outvars:
      if not v in used:
        varnames[v] = '_'
    used.update(atom for atom in eqn.invars if isinstance(atom, Var))
  return varnames

