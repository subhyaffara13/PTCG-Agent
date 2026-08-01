
def _jaxpr_call_abstract_eval(*args, jaxpr: jax_core.Jaxpr, **params):
  del args, params  # Unused.
  # Filter out input effects, since they are only relevant in the context
  # of this ``jaxpr_call``.
  out_effects = {
      e for e in jaxpr.effects if not isinstance(e, effects.JaxprInputEffect)
  }
  return jaxpr.out_avals, out_effects

