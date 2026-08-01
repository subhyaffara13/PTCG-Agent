
def _stage_jaxpr_abstract_eval(*_, jaxpr):
  return jaxpr.out_avals, core.positional_effects(jaxpr)

