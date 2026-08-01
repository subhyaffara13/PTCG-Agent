
def _decay_rate_pow(
    i: jax.typing.ArrayLike, exponent: jax.typing.ArrayLike = 0.8) -> jax.Array:
  """Second-order moment decay schedule."""
  t = jnp.array(i + 1, jnp.float32)
  return 1.0 - t ** (-exponent)

