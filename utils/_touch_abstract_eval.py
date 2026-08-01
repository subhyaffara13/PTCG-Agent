
def _touch_abstract_eval(ref: jax.Array):
  return [], {state.ReadEffect(0), state.WriteEffect(0)}

