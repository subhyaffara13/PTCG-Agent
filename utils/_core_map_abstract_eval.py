
def _core_map_abstract_eval(*args, jaxpr, mesh, interpret, **kwargs):
  del args
  if jaxpr.outvars:
    raise ValueError("core_map must not return any outputs.")
  effs = {*get_interpret_effects(interpret)}
  constvar_idx = {v: i for i, v in enumerate(jaxpr.constvars)}
  for eff in jaxpr.effects:
    if mesh.discharges_effect(eff) or isinstance(eff, CommsEffect):
      continue
    if kernel_local_effects.contains(eff):
      continue
    if isinstance(eff, effects.JaxprInputEffect):
      # The eqn's inputs are the jaxpr's constvars (closed-over refs).
      if eff.input in constvar_idx:
        effs.add(eff.replace(constvar_idx[eff.input]))
      continue
    if not isinstance(eff, jax_core.NamedAxisEffect):
      effs.add(eff)
      continue
    if eff.name not in mesh.shape:
      effs.add(eff)
  return [], effs

