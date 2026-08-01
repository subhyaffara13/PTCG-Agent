
def eqns_using_var(jaxpr: core.Jaxpr, invar: core.Var) -> Iterator[core.JaxprEqn]:
  """Find the leaf equations using a variable"""
  # The complexity of this call is because the invar might originate from a nested jaxpr
  for eqn, invar_index in eqns_using_var_with_invar_index(jaxpr, invar):
    if (child_jaxprs_and_vars := tuple(jaxpr_and_binder_in_params(eqn.params, invar_index))):
      for (jaxpr, invar) in child_jaxprs_and_vars:
        yield from eqns_using_var(jaxpr, invar)
    else:
      # if the previous condition fails, there is no deeper jaxpr to explore =(
      yield eqn

