
def _pjit_abstract_eval(*args, jaxpr, out_shardings, **_):
  return jaxpr.out_avals, core.positional_effects(jaxpr)

