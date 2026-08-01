
def compute_amax_history(x, amax_history):
  amax_update = jnp.max(jnp.abs(x)).astype(amax_history.dtype)
  new_history = jnp.roll(amax_history, shift=-1, axis=0).at[0].set(amax_update)
  return new_history

