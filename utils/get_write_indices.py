
def get_write_indices(jaxpr):
  effects = set()
  all_vars = {v: i for i, v in enumerate(jaxpr.constvars + jaxpr.invars)}
  for eqn in jaxpr.eqns:
    for e in eqn.effects:
      if isinstance(e, (state_types.WriteEffect, state_types.AccumEffect)):
        if (idx := all_vars.get(e.input, None)) is not None:
          effects.add(idx)
  return effects

