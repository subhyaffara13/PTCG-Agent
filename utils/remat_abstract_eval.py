
def remat_abstract_eval(*args, jaxpr, prevent_cse, differentiated, policy):
  del args, prevent_cse, differentiated, policy  # Unused.
  return [v.aval for v in jaxpr.outvars], core.positional_effects(jaxpr)

