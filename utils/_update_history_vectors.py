
def _update_history_vectors(history, new):
  # TODO(Jakob-Unfried) use rolling buffer instead? See #6053
  return jnp.roll(history, -1, axis=0).at[-1, :].set(new)

