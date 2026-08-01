
def subst_input_effects(effs, env) -> Effects:
  return {e.replace(env.get(e.input, e.input))
          if isinstance(e, effects.JaxprInputEffect) else e for e in effs}

