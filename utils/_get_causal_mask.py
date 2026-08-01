
def _get_causal_mask(T, S):
  mask = jnp.tril(jnp.ones((T, S), dtype=bool))
  return mask[None, None, :, :]

