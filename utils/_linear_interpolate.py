
def _linear_interpolate(
    start: jax.typing.ArrayLike,
    end: jax.typing.ArrayLike,
    pct: jax.typing.ArrayLike):
  """Linearly interpolate between two values."""
  return (end - start) * pct + start

