
def eqns_using_var_with_invar_index(jaxpr: core.Jaxpr, invar: core.Var) -> Iterator[tuple[core.JaxprEqn, int]]:
  """Find all the equations which use invar and the positional index of its binder"""
  for eqn in jaxpr.eqns:
    for invar_index, eqn_var in enumerate(eqn.invars):
      if eqn_var == invar:
        yield eqn, invar_index
        break # we found the var, no need to keep looking in this eqn

