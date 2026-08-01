
def _parallel_loop_abstract_eval(*args, jaxpr, tree, **params):
  del params  # Unused.
  _, _, _, _, carries = tree.unflatten(args)
  if any(isinstance(c, (Ref, TransformedRef)) for c in carries):
    raise TypeError(f"Carried values may not be refs, but got: {carries}")
  updated_effects = set()
  for eff in jax_core.positional_effects(jaxpr):
    if isinstance(eff, effects.JaxprInputEffect):
      # Offset for the parallel_loop eqn to account for start, stop, and step
      # args passed to parallel_loop_p.bind.
      eff = eff.replace(eff.input + 3)
    updated_effects.add(eff)
  return carries, updated_effects

