
def _magicbox(x):
  """MagicBox operator."""
  return jnp.exp(x - jax.lax.stop_gradient(x))

