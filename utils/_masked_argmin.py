
def _masked_argmin(array, mask):
  array = jnp.where(mask, array, jnp.inf)
  assert isinstance(array, jax.Array)
  return jnp.argmin(array)

