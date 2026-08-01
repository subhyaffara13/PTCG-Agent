
def _zeros_like_no_axis(x, axis: int) -> jax.Array:
  """Returns an array of zeros like x, with the given axis of `x` removed."""
  # The logic here is unusual to circumvent sharding-in-types limitations.
  # We use jax.eval_shape to get the shape/sharding of an array with the given
  # axis removed.
  target = jax.eval_shape(lambda x: jnp.sum(x, axis=axis), x)
  return jnp.zeros_like(target)

