
def _zeros_like_axis(x, axis: int) -> jax.Array:
  """Returns an array of zeros like the given axis of `x`."""
  # The logic here is unusual to circumvent sharding-in-types limitations.
  # We use jax.eval_shape to get the shape/sharding of the given axis of `x`.
  axes = tuple(i for i in range(x.ndim) if i != axis)
  target = jax.eval_shape(functools.partial(jnp.sum, axis=axes), x)
  return jnp.zeros_like(target)

