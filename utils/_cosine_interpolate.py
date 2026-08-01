
def _cosine_interpolate(
    start: jax.typing.ArrayLike,
    end: jax.typing.ArrayLike,
    pct: jax.typing.ArrayLike):
  """Cosine interpolate between two values (smoother transitions)."""
  return end + (start - end) / 2.0 * (jnp.cos(jnp.pi * pct) + 1)

