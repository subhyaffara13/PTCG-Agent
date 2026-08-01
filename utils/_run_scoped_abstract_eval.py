
def _run_scoped_abstract_eval(*args, jaxpr, collective_axes, **_):
  del args, collective_axes
  # jaxpr will have effects for its inputs (Refs that are allocated) and for
  # constvars (closed over Refs). The effects for the allocated Refs are local
  # to the jaxpr and shouldn't propagate out. The eqn's inputs are the jaxpr's
  # constvars, so effects on constvars propagate by constvar position.
  constvar_idx = {v: i for i, v in enumerate(jaxpr.constvars)}
  nonlocal_effects = set()
  for eff in jaxpr.effects:
    if isinstance(eff, effects.JaxprInputEffect):
      if eff.input in constvar_idx:
        nonlocal_effects.add(eff.replace(constvar_idx[eff.input]))
      continue
    nonlocal_effects.add(eff)
  return [v.aval for v in jaxpr.outvars], nonlocal_effects

